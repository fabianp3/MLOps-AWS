from flask import Flask, render_template
import os
import random

app = Flask(__name__)

# list of cat images
images = [
    "https://github.com/CamilaCortex/MLOps-AWS/blob/main/Dockers/flask-app/images/image1.gif",
    "https://github.com/CamilaCortex/MLOps-AWS/blob/main/Dockers/flask-app/images/image2.gif",
    "https://github.com/CamilaCortex/MLOps-AWS/blob/main/Dockers/flask-app/images/image3.gif",
]


@app.route("/")
def index():
    url = random.choice(images)
    return render_template("index.html", url=url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))