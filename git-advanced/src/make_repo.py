"""Builds the pay-calculator practice repo with exactly the commit IDs used in the lessons.
Usage: python make_repo.py <empty output folder>
The file contents, dates, author and messages below were checked against every commit ID the lessons show."""
import os, subprocess, sys
from base import R1, R2, R3, P1, P2, P3, P4, P5, T1, T2, GI, CON
AUTHOR = ("Sam Lee", "12345678+sam-lee@users.noreply.github.com")
STEPS = [  # (February day, message, files changed)
    (2, "Add README", {"README.md": R1}),
    (3, "Add basic shift pay", {"pay.py": P1}),
    (4, "Add tests", {"test_pay.py": T1}),
    (5, "Add weekend rates", {"pay.py": P2}),
    (6, "Test weekend rates", {"test_pay.py": T2}),
    (7, "Ignore Python cache and .env", {".gitignore": GI}),
    (8, "Add docstring", {"pay.py": P3}),
    (9, "Tidy weekend rate names", {"pay.py": P4}),
    (10, "Update README", {"README.md": R2}),
    (11, "Reject negative hours", {"pay.py": P5}),
    (12, "Add note about award rates", {"README.md": R3}),
    (13, "Add contributing guide", {"CONTRIBUTING.md": CON}),
]
EXPECTED = "40bd88bb826cba6f912a7acf45382e462c5b7e23"
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
def git(*args, day=None, check=True):
    env = dict(os.environ, GIT_AUTHOR_NAME=AUTHOR[0], GIT_AUTHOR_EMAIL=AUTHOR[1], GIT_COMMITTER_NAME=AUTHOR[0],
               GIT_COMMITTER_EMAIL=AUTHOR[1], GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")
    if day:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"2026-02-{day:02d}T10:00:00+11:00"
    return subprocess.run(["git", *args], cwd=out, env=env, check=check, capture_output=True, text=True).stdout.strip()
git("init", "-q", "-b", "main")
for day, msg, files in STEPS:
    for name, text in files.items():
        with open(os.path.join(out, name), "w", newline="\n", encoding="utf-8") as f:
            f.write(text)
    git("add", "-A")
    git("commit", "-q", "-m", msg, day=day)
    if msg == "Test weekend rates":
        v10 = git("rev-parse", "HEAD")
git("tag", "-a", "v1.0", "-m", "First release", v10, day=14)
head = git("rev-parse", "HEAD")
assert head == EXPECTED, head
# Module 7 (leaked secret): a branch where someone forced a .env file in. Not shown with IDs in the lessons.
git("switch", "-q", "-c", "leaked-key")
with open(os.path.join(out, ".env"), "w", newline="\n") as f:
    f.write("PAYMENTS_API_KEY=practice-only-not-a-real-key-7f3a9c\n")
git("add", "-f", ".env")
git("commit", "-q", "-m", "Add config for the payments API", day=15)
with open(os.path.join(out, "README.md"), "a", newline="\n") as f:
    f.write("\n## Run the tests\n\n    python test_pay.py\n")
git("commit", "-q", "-am", "Explain how to run the tests", day=16)
git("switch", "-q", "main")
git("gc", "-q", "--prune=now")
print("pay-calculator ready:", head[:7])
