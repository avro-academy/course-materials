"""Information about each document that the text doesn't say: its title, what kind it is, when it was updated,
and whether it's still current. Old versions stay in the folder but are marked current: False."""

DOCUMENTS = {
    "Corner-Cafe-Staff-Handbook-2026.pdf": {"title": "Staff Handbook (2026)", "kind": "handbook", "updated": "2026-07-01", "current": True},
    "Corner-Cafe-Staff-Handbook-2024.pdf": {"title": "Staff Handbook (2024, replaced)", "kind": "handbook", "updated": "2024-07-01", "current": False},
    "Food-Safety-Program.pdf": {"title": "Food Safety Program", "kind": "procedure", "updated": "2026-03-01", "current": True},
    "Espresso-Machine-Guide.pdf": {"title": "Espresso Machine Guide", "kind": "procedure", "updated": "2026-02-01", "current": True},
    "Refunds-and-Complaints-Policy.docx": {"title": "Refunds and Complaints Policy", "kind": "policy", "updated": "2025-11-01", "current": True},
    "Privacy-Policy.docx": {"title": "Privacy and CCTV Policy", "kind": "policy", "updated": "2025-11-01", "current": True},
    "Staff-FAQ.md": {"title": "Staff FAQ", "kind": "faq", "updated": "2026-07-01", "current": True},
}


def info(source):
    """Metadata for a file; unknown files are treated as current, with their file name as the title."""
    return DOCUMENTS.get(source, {"title": source, "kind": "other", "updated": "", "current": True})


if __name__ == "__main__":
    for name, meta in DOCUMENTS.items():
        print(f"{name:<38} {meta['updated']}  {'current' if meta['current'] else 'REPLACED'}  {meta['title']}")
