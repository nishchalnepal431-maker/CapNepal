from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    caption = ""
    hashtags = ""
    if request.method == "POST":
        user_input = request.form.get("video_topic")
        if user_input:
            caption = f"🔥 यो भिडियो वास्तवमै खतरा छ! - {user_input} 🚀"
            hashtags = "#NishchalTech #CapNepal #Trending #Nepal #ViralReels #FYP"
            
    return render_template("index.html", caption=caption, hashtags=hashtags)

if __name__ == "__main__":
    app.run(debug=True)
