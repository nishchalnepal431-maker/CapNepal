import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Whisper AI मोडेल लोड गर्ने
print("Loading Whisper Model...")
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def home():
    output_video = ""
    if request.method == "POST":
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(video_path)
                
                # १. Whisper मार्फत अडियो ट्रान्सक्राइब गर्ने र टाइमस्ट्याम्प निकाल्ने
                result = model.transcribe(video_path)
                
                # २. भिडियो क्लिप लोड गर्ने
                video = VideoFileClip(video_path)
                clips = [video]
                
                # ३. प्रत्येक शब्द वा वाक्यलाई भिडियोको माथि टेक्स्टको रूपमा राख्ने
                for segment in result['segments']:
                    text = segment['text'].strip()
                    start_time = segment['start']
                    end_time = segment['end']
                    
                    # टिकटक स्टाइलको टेक्स्ट क्लिप बनाउने
                    txt_clip = (TextClip(text, fontsize=50, color='white', font='Arial-Bold', stroke_color='black', stroke_width=2)
                                .set_position(('center', 100)) # भिडियोको माथिल्लो भागमा देखाउने
                                .set_start(start_time)
                                .set_end(end_time))
                    clips.append(txt_clip)
                
                # ४. नयाँ सबटाइटल सहितको भिडियो सेभ गर्ने
                output_filename = "subtitled_" + filename
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                
                final_video = CompositeVideoClip(clips)
                final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
                
                output_video = output_filename
                
    return render_template("index.html", output_video=output_video)

@app.route('/outputs/<filename>')
def downloaded_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
