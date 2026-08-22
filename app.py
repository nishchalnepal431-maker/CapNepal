import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

# अपलोड गर्ने फोल्डर मिलाउने
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def home():
    caption = ""
    hashtags = ""
    filename = ""
    
    if request.method == "POST":
        # प्रयोगकर्ताले भिडियो अपलोड गरे, नगरेको चेक गर्ने
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
                # एआई मार्फत जेनेरेट भएको क्याप्सन (स्टाइलिस टेक्स्ट)
                caption = f"🔥 यो भिडियो ({filename}) त एकदमै खतरा र भाइरल हुनेवाला छ! 🚀"
                hashtags = "#NishchalTech #CapNepal #TrendingNepal #ViralReels #FYP #TikTokNepal"
                
    return render_template("index.html", caption=caption, hashtags=hashtags, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
