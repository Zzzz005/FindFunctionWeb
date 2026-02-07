import re
from pathlib import Path
import pdfplumber
from docx import Document

# Папка проекта — где лежит скрипт
base_dir = Path(__file__).parent

# Регулярка: слово начинается с f_, перед ним нет $
pattern = re.compile(r"(?<!\$)\bf_\w+\b")

# Функция для чтения текста из файла
def read_text(file: Path) -> str:
    if file.suffix in [".txt", ".php", ".bas", ".py"]:
        return file.read_text(encoding="utf-8", errors="ignore")

    elif file.suffix == ".pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    elif file.suffix == ".docx":
        doc = Document(file)
        return "\n".join(p.text for p in doc.paragraphs)

    return ""  # для остальных файлов

# Обход всех файлов в папке
for file in base_dir.iterdir():
    if not file.is_file():
        continue

    if file.suffix.lower() not in [".txt", ".php", ".bas", ".py", ".pdf", ".docx"]:
        continue

    try:
        text = read_text(file)
    except Exception as e:
        print(f"[SKIP] {file.name} ({e})")
        continue

    matches = sorted(set(pattern.findall(text)))

    if matches:
        print(f"\n📄 Файл: {file.name}")
        for m in matches:
            print("  ", m)
