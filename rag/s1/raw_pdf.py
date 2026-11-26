from pypdf import PdfReader

text = PdfReader("docs/Corner-Cafe-Staff-Handbook-2026.pdf").pages[2].extract_text()
print(text[:150])
print("...")
print(text[-110:])
print()
print("Is 'staff' in it?", "staff" in text)
