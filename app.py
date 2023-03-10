from flask import Flask, render_template, request, send_file
from pytube import YouTube
from zipfile import ZipFile
import os
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.form["url"]
    try:
        yt = YouTube(url)
    except:
        return render_template("index.html", error=True)
    try:
        stream = yt.streams.get_by_itag(251)
        file_path = stream.download(output_path="./")
        filename = f"{yt.title}.mp4"
        os.rename(file_path, filename)
        return send_file(filename, as_attachment=True)
    except:
        return render_template("index.html", error=True)

if __name__ == "__main__":
    app.run(debug=True)
