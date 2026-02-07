import re
from flask import Flask, request, render_template
import pdfplumber
from docx import Document
import os


app = Flask(__name__)

# Регулярка: f_ в начале слова, перед ним нет $
pattern = re.compile(r"(?<!\$)\bf_\w+\b")

def extract_text(file):
    filename = file.filename.lower()
    
    if filename.endswith((".txt", ".php", ".bas", ".py")):
        return file.read().decode('utf-8', errors='ignore')
    
    elif filename.endswith(".pdf"):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    elif filename.endswith(".docx"):
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)
    
    return ""

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        uploaded_file = request.files.get("file")
        if uploaded_file:
            text = extract_text(uploaded_file)
            matches = sorted(set(pattern.findall(text)))
            results = matches
    return render_template("index.html", results=results)

#if __name__ == "__main__":
#    app.run(debug=True)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

