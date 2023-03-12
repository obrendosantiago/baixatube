from flask import Flask, render_template, request, send_file
from pytube import YouTube, Playlist
import os
import zipfile
import re

app = Flask(__name__)

@app.route('/baixatube/index.html')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    is_playlist = 'list=' in url
    try:
        if is_playlist:
            pl = Playlist(url)
        else:
            yt = YouTube(url)
    except:
        return render_template('index.html', error=True)

    if is_playlist:
        title = pl.title.replace('/', '')
        zip_filename = f'{title}.zip'
        zip_path = os.path.join('downloads', zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for video in pl.videos:
                stream = video.streams.get_by_itag(251)
                video_title = re.sub('[^\w\-_\. ]', '', video.title) # substitui caracteres inválidos por um caractere vazio
                filename = f'{video_title}.mp3'
                stream.download(filename=os.path.join('downloads', filename))
                zip_file.write(os.path.join('downloads', filename), arcname=filename)
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)

    else:
        title = yt.title.replace('/', '')
        stream = yt.streams.get_by_itag(251)
        filename = re.sub('[^\w\-_\. ]', '', f'{title}.mp3') # substitui caracteres inválidos por um caractere vazio
        stream.download(filename=os.path.join('downloads', filename))
        if os.path.isfile(os.path.join('downloads', filename)):
            return send_file(os.path.join('downloads', filename), as_attachment=True, download_name=filename)
        else:
            return render_template('index.html', error=True)

if __name__ == '__main__':
    app.run(debug=True)
