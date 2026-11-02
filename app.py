from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>InstaProMax</title>
<style>
body {
    margin: 0;
    font-family: Arial;
    background: #101426;
    color: white;
    text-align: center;
}
header {
    padding: 25px;
    background: #202b50;
    font-size: 30px;
    font-weight: bold;
}
h2 { margin-top: 35px; }
.box {
    background: #202b50;
    margin: 20px;
    padding: 25px;
    border-radius: 18px;
}
input {
    width: 90%;
    padding: 14px;
    border: 0;
    border-radius: 10px;
    box-sizing: border-box;
}
button {
    background: #2878ff;
    color: white;
    border: 0;
    padding: 13px 25px;
    border-radius: 10px;
    margin-top: 15px;
    font-size: 16px;
}
footer { padding: 25px; color: #aaa; }
</style>
</head>
<body>
<header>🚀 InstaProMax</header>
<h2>All Video Tools in One Place</h2>

<div class="box">
<h2>🔴 YouTube Downloader</h2>
<form action="/download" method="post">
<input type="url" name="url" placeholder="Paste YouTube link" required>
<input type="hidden" name="platform" value="YouTube">
<button>Download</button>
</form>
</div>

<div class="box">
<h2>📸 Instagram Downloader</h2>
<form action="/download" method="post">
<input type="url" name="url" placeholder="Paste Instagram link" required>
<input type="hidden" name="platform" value="Instagram">
<button>Download</button>
</form>
</div>

<div class="box">
<h2>🔵 Facebook Downloader</h2>
<form action="/download" method="post">
<input type="url" name="url" placeholder="Paste Facebook link" required>
<input type="hidden" name="platform" value="Facebook">
<button>Download</button>
</form>
</div>

<footer>© 2026 InstaProMax</footer>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/download", methods=["POST"])
def download():
    return "Downloader setup is coming soon!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
