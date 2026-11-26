How the documents were made

The seven Corner Café documents are made up, for the course. Their words are in docs_content.py, and make_docs.py
turns them into the PDFs (through a web browser), the Word files and the Markdown file.

To change a fact and rebuild the documents (lesson 17's "Try it"):

  pip install playwright python-docx
  playwright install chromium
  python make_docs.py ../step-6-web/docs      (or whichever step's docs folder you're using)

Then run python index.py again in that step's folder. The PDFs use the DejaVu fonts if your computer has them;
with other fonts, line breaks and page counts can differ a little from the lessons.
