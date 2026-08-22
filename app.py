import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

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
                
                # स्टाइलिस क्याप्सन र ह्याशट्याग जेनेरेटर
                caption = f"🔥 ({filename}) भिडियो अब TikTok र Reels मा भाइरल हुनेवाला छ! 🚀"
                hashtags = "#NishchalTech #CapNepal #TrendingNepal #ViralReels #FYP #TikTokNepal"
                
    return render_template("index.html", caption=caption, hashtags=hashtags, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
