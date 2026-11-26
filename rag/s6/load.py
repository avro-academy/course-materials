"""Step 1: get the text out of PDFs, Word files and Markdown, page by page, and tidy it up.

Run it to see how much text each document has:  python load.py
"""
import os
import re
import unicodedata
from collections import Counter

from docx import Document
from pypdf import PdfReader

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")


def clean(text):
    """Tidy text from PDFs and Word files: join ligatures (ﬀ → ff), fix spacing and broken lines."""
    text = unicodedata.normalize("NFKC", text)        # ﬁ, ﬀ and other special characters → normal letters
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)       # words split across lines with a hyphen
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


PAGE_NUMBER = re.compile(r"^(page\s*)?\d+(\s*(of|/)\s*\d+)?$", re.IGNORECASE)


def remove_headers_and_footers(texts):
    """Lines printed on every page (a running header or footer) and page numbers aren't content: drop them."""
    counts = Counter(line.strip() for text in texts for line in set(text.split("\n")))
    repeated = {line for line, n in counts.items() if line and len(texts) > 1 and n == len(texts)}
    return ["\n".join(line for line in text.split("\n")
                      if line.strip() not in repeated and not PAGE_NUMBER.match(line.strip())) for text in texts]


def load_pdf(path):
    texts = remove_headers_and_footers([page.extract_text() or "" for page in PdfReader(path).pages])
    return [{"page": n, "text": clean(text)} for n, text in enumerate(texts, start=1)]


def load_docx(path):
    """A Word file has no pages, so it becomes one piece. Headings are marked with ## so they can be found later."""
    lines = []
    for p in Document(path).paragraphs:
        if not p.text.strip():
            continue
        lines.append(("## " if p.style.name.startswith("Heading") or p.style.name == "Title" else "") + p.text)
    return [{"page": None, "text": clean("\n".join(lines))}]


def load_markdown(path):
    with open(path, encoding="utf-8") as f:
        return [{"page": None, "text": clean(f.read())}]


LOADERS = {".pdf": load_pdf, ".docx": load_docx, ".md": load_markdown}


def load_documents(folder=DOCS):
    """Every page (or whole file) of every document, as {"source", "page", "text"}."""
    pages = []
    for name in sorted(os.listdir(folder)):
        loader = LOADERS.get(os.path.splitext(name)[1].lower())
        if loader:
            for piece in loader(os.path.join(folder, name)):
                if piece["text"]:
                    pages.append({"source": name, **piece})
    return pages


if __name__ == "__main__":
    pages = load_documents()
    for name in sorted({p["source"] for p in pages}):
        mine = [p for p in pages if p["source"] == name]
        words = sum(len(p["text"].split()) for p in mine)
        print(f"{name:<38}{len(mine):>3} page(s) {words:>6} words")
    print(len(pages), "pieces in total")
