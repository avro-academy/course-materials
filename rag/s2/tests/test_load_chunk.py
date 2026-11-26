"""Tests for loading and chunking. They use small made-up texts, so they run in a second: python -m pytest"""
from chunk import chunk_pages, fixed_chunks, is_heading, sections
from load import clean, remove_headers_and_footers


def test_clean_joins_ligatures_and_broken_words():
    assert clean("Casual staﬀ get a ﬁxed rate") == "Casual staff get a fixed rate"
    assert clean("a 30-\nminute break") == "a 30minute break"  # why documents avoid hyphens at line ends
    assert clean("too    many   spaces") == "too many spaces"


def test_headers_footers_and_page_numbers_are_removed():
    pages = ["Corner Café Staff Handbook\nPay day\nPage 1 of 2", "Corner Café Staff Handbook\nBreaks\nPage 2 of 2"]
    assert remove_headers_and_footers(pages) == ["Pay day", "Breaks"]


def test_headings():
    assert is_heading("2.3 Breaks")
    assert is_heading("## Who do I talk to about a pay problem, and how quickly will it be fixed?")
    assert not is_heading("Water leaking around the")      # a table row that wrapped
    assert not is_heading("2 weeks ahead if you can't work.")
    assert not is_heading("1.1 Types of employment and what each type means for your pay and leave")  # too long


def test_sections_split_at_headings():
    assert sections("2.1 Rosters\nIn Deputy.\n2.2 Swapping shifts\nAsk first.") == [
        ("2.1 Rosters", "In Deputy."), ("2.2 Swapping shifts", "Ask first.")]


def test_fixed_chunks_overlap():
    words = " ".join(str(n) for n in range(10))
    assert fixed_chunks(words, size=4, overlap=1) == ["0 1 2 3", "3 4 5 6", "6 7 8 9"]


def test_a_section_keeps_its_heading_on_the_next_page():
    pages = [{"source": "h.pdf", "page": 1, "text": "2.3 Breaks\nA 30 minute meal break."},
             {"source": "h.pdf", "page": 2, "text": "And a 10 minute rest break."},
             {"source": "other.pdf", "page": 1, "text": "No heading here."}]
    chunks = chunk_pages(pages)
    assert [c["section"] for c in chunks] == ["2.3 Breaks", "2.3 Breaks", ""]
    assert chunks[1]["text"] == "2.3 Breaks\nAnd a 10 minute rest break."
    assert len({c["id"] for c in chunks}) == 3
