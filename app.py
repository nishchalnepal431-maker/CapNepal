import os
from flask import Flask, render_template, request
from werkzeug.utils import secure
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Whisper AI मोडेल लोड गर्ने (पहिलो पटक चल्दा अलि समय लिन सक्छ)
print("Loading Whisper AI Model...")
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def home():
    result_text = ""
    filename = ""
    
    if request.method == "POST":
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(video_path)
                
                # भिडियोको अडियो ट्रान्सक्राइब गर्ने
                try:
                    print(f"Transcribing {filename}...")
                    audio_result = model.transcribe(video_path)
                    result_text = audio_result['text']
                except Exception as e:
                    result_text = f"एरर आयो: {str(e)}"
                
    return render_template("index.html", result_text=result_text, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
