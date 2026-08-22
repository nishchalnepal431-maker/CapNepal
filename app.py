import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# अपलोड फोल्डर मिलाउने
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    caption = ""
    hashtags = ""
    filename = ""
    
    if request.method == "POST":
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # एआई क्याप्सन र ह्याशट्यागहरू
                caption = f"🔥 यो भिडियो ({filename}) त एकदमै खतरा र भाइरल हुनेवाला छ! 🚀"
                hashtags = "#NishchalTech #CapNepal #TrendingNepal #ViralReels #FYP #TikTokNepal"
                
    return render_template("index.html", caption=caption, hashtags=hashtags, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
