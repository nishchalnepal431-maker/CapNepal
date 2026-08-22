import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import openai

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# OpenAI API Key राख्ने (तपाईंले आफ्नो OpenAI अकाउन्टबाट लिएर यहाँ राख्नुपर्छ)
# वा Render को Environment Variables मा OPENAI_API_KEY भनेर राख्न सक्नुहुन्छ
openai.api_key = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")

@app.route("/", methods=["GET", "POST"])
def home():
    transcription = ""
    filename = ""
    
    if request.method == "POST":
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(video_path)
                
                try:
                    # OpenAI Whisper API मार्फत छिटो ट्रान्सक्राइब गर्ने
                    with open(video_path, "rb") as audio_file:
                        response = openai.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file
                        )
                        transcription = response.text
                except Exception as e:
                    transcription = f"एरर आयो: {str(e)}"
                
    return render_template("index.html", transcription=transcription, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
