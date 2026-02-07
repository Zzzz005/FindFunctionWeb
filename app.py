import re
from flask import Flask, request, render_template
import pdfplumber
from docx import Document
import os
import tempfile

app = Flask(__name__)

# Регулярка: f_ в начале слова, перед ним нет $
pattern = re.compile(r"(?<!\$)\bf_\w+\b")

def extract_text(file):
    filename = file.filename.lower()

    # Сохраняем временный файл для обработки
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    text = ""
    try:
        if filename.endswith((".txt", ".php", ".bas", ".py")):
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif filename.endswith(".pdf"):
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        elif filename.endswith(".docx"):
            doc = Document(tmp_path)
            text = "\n".join(p.text for p in doc.paragraphs)
    finally:
        os.remove(tmp_path)  # удаляем временный файл

    return text

@app.route("/", methods=["GET", "POST"])
def index():
    results_by_file = {}
    if request.method == "POST":
        uploaded_files = request.files.getlist("files")
        for file in uploaded_files:
            text = extract_text(file)
            matches = sorted(set(pattern.findall(text)))
            results_by_file[file.filename] = matches

    return render_template("index.html", results_by_file=results_by_file)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
