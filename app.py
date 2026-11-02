from flask import Flask, request, render_template_string, send_file
import yt_dlp
import tempfile
import os
import glob
import shutil
from urllib.parse import urlparse

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>InstaProMax Downloader</title>

<style>
* {
    box-sizing: border-box;
}
body {
    margin: 0;
    font-family: Arial;
    background: #07152e;
    color: white;
    text-align: center;
}
header {
    padding: 25px;
    font-size: 30px;
    font-weight: bold;
    color: #00c8ff;
}
.container {
    max-width: 500px;
    margin: 40px auto;
    padding: 25px;
}
h1 {
    font-size: 28px;
}
p {
    color: #b8c8e5;
}
input {
    width: 100%;
    padding: 17px;
    border-radius: 10px;
    border: none;
    margin-top: 20px;
    font-size: 15px;
}
button {
    width: 100%;
    padding: 16px;
    background: #008cff;
    color: white;
    border: none;
    border-radius: 10px;
    margin-top: 15px;
    font-size: 18px;
    font-weight: bold;
}
button:active {
    background: #005bbb;
}
.box {
    background: #10264a;
    padding: 20px;
    border-radius: 15px;
    margin-top: 25px;
}
.error {
    color: #ff7777;
    margin-top: 20px;
}
footer {
    margin-top: 70px;
    color: #8295b5;
    font-size: 13px;
}
</style>
</head>

<body>

<header>InstaProMax</header>

<div class="container">

<h1>Video Downloader</h1>

<p>YouTube, Instagram और Facebook के समर्थित वीडियो लिंक यहाँ डालें।</p>

<div class="box">

<form action="/download" method="POST">

<input
type="url"
name="url"
placeholder="Paste Video Link Here..."
required>

<button type="submit">
Download Video
</button>

</form>

{% if error %}
<div class="error">{{ error }}</div>
{% endif %}

</div>

<footer>
InstaProMax © 2026
<br><br>
Only download content you own or are authorized to download.
</footer>

</div>
</body>
</html>
"""


ALLOWED_DOMAINS = [
    "youtube.com",
    "youtu.be",
    "instagram.com",
    "facebook.com",
    "fb.watch"
]


def valid_url(url):
    try:
        parsed = urlparse(url)

        if parsed.scheme != "https":
            return False

        if not parsed.hostname:
            return False

        if parsed.username or parsed.password:
            return False

        if parsed.port not in (None, 443):
            return False

        host = parsed.hostname.lower()

        return any(
            host == domain or host.endswith("." + domain)
            for domain in ALLOWED_DOMAINS
        )

    except ValueError:
        return False


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url", "").strip()

    if not valid_url(url):
        return render_template_string(
            HTML,
            error="कृपया सही समर्थित HTTPS वीडियो लिंक डालें।"
        )

    folder = tempfile.mkdtemp(prefix="instapromax_")

    try:

        options = {
            "format": "best[ext=mp4]/best",
            "outtmpl": os.path.join(
                folder, "%(title).80s.%(ext)s"
            ),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "max_filesize": 100 * 1024 * 1024,
            "socket_timeout": 20,
            "retries": 1
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])

        files = glob.glob(os.path.join(folder, "*"))

        if not files:
            raise Exception("Video file नहीं मिली।")

        filepath = files[0]

        response = send_file(
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath)
        )

        response.call_on_close(
            lambda: shutil.rmtree(folder, ignore_errors=True)
        )

        return response

    except Exception:
        shutil.rmtree(folder, ignore_errors=True)

        return render_template_string(
            HTML,
            error="डाउनलोड नहीं हो पाया। यह लिंक समर्थित नहीं है या वीडियो उपलब्ध नहीं है।"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


