import re
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# f_ в начале слова, без $
pattern = re.compile(r"(?<!\$)\bf_\w+\b")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    matches = sorted(set(pattern.findall(text)))
    return jsonify(matches)

if __name__ == "__main__":
    app.run()
