"""Step 2: split documents into chunks — pieces about one thing each — that keep their source, page and section.

Run it to see how many chunks there are:  python chunk.py
"""
import re

MAX_WORDS = 150  # a section longer than this is split into pieces of about this many words
OVERLAP = 30     # words repeated at the start of the next piece, so a sentence cut at the edge appears whole once


def fixed_chunks(text, size=MAX_WORDS, overlap=OVERLAP):
    """The simple way: every `size` words, whatever they say."""
    words = text.split()
    step = size - overlap
    return [" ".join(words[i:i + size]) for i in range(0, max(len(words) - overlap, 1), step)]


# A heading is a Markdown/Word heading (# …) or a numbered one, like "2.3 Breaks". Other short lines (table rows
# that wrapped, for example) look like headings to a computer, so they don't count.
HEADING = re.compile(r"^\d+(\.\d+)*\.?\s+[A-Z].{2,60}$")


def is_heading(line):
    line = line.strip()
    if line.startswith("#"):  # Markdown and Word headings are always headings
        return True
    return len(line.split()) <= 8 and not line.endswith((".", ",", ":")) and bool(HEADING.match(line))


def sections(text):
    """Split a page at its headings: [(heading, body), ...]."""
    found, heading, body = [], "", []
    for line in text.split("\n"):
        if is_heading(line):
            if " ".join(body).strip():
                found.append((heading, "\n".join(body).strip()))
            heading, body = line.lstrip("#").strip(), []
        else:
            body.append(line)
    if " ".join(body).strip():
        found.append((heading, "\n".join(body).strip()))
    return found


def chunk_pages(pages):
    """Chunks that follow the document's structure: one per section, split further only if a section is long.
    Each chunk starts with its heading, so it makes sense on its own."""
    chunks, current_heading, current_source = [], "", None
    for page in pages:
        if page["source"] != current_source:  # a new document: no heading yet
            current_heading, current_source = "", page["source"]
        for heading, body in sections(page["text"]):  # a section can carry on onto the next page
            current_heading = heading or current_heading
            for piece in fixed_chunks(body):
                text = f"{current_heading}\n{piece}" if current_heading else piece
                chunks.append({"source": page["source"], "page": page["page"], "section": current_heading, "text": text})
    for n, c in enumerate(chunks):
        c["id"] = f"{c['source']}#{c['page'] or 0}#{n}"
    return chunks


if __name__ == "__main__":
    import textwrap

    from load import load_documents

    chunks = chunk_pages(load_documents())
    sizes = [len(c["text"].split()) for c in chunks]
    print(f"{len(chunks)} chunks; words per chunk: smallest {min(sizes)} average {sum(sizes) // len(sizes)} largest {max(sizes)}")
    for c in chunks:
        if c["section"] in ("1.2 Pay rates", "1.3 Pay day and payslips", "2.1 Rosters"):
            heading, body = c["text"].split("\n", 1)
            print(f"\n--- {c['source']} page {c['page']} | {c['section']}\n{heading}")
            print(textwrap.fill(" ".join(body.split())[:288], 120))
