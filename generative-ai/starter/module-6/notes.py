"""Load Brightside's notes and split them into chunks: one chunk per heading section."""
from pathlib import Path

NOTES_DIR = Path(__file__).resolve().parent.parent / "data" / "brightside-notes"


def load_chunks():
    chunks = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        title = ""
        section = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                if section:
                    chunks.append({"source": path.name, "title": title, "text": "\n".join(section).strip()})
                title = line.lstrip("# ").strip()
                section = [line]
            else:
                section.append(line)
        if section:
            chunks.append({"source": path.name, "title": title, "text": "\n".join(section).strip()})
    return [c for c in chunks if len(c["text"].split()) > 5]


if __name__ == "__main__":
    for chunk in load_chunks():
        print(f"{chunk['source']:20} {chunk['title']:35} {len(chunk['text'].split())} words")
