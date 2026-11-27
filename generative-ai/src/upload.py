"""Create the Generative AI course on avro.academy as a DRAFT (never published here)."""
import json, os, sys, hashlib
import httpx

BASE = "https://avro.academy"
H = {"Authorization": "users API-Key " + os.environ["AVRO_ACADEMY_API_KEY"]}
c = httpx.Client(base_url=BASE, headers=H, timeout=120)
STATE = "state.json"
state = json.load(open(STATE)) if os.path.exists(STATE) else {}
def save(): json.dump(state, open(STATE, "w"), indent=1)

def check(r):
    if r.status_code >= 300:
        print(r.status_code, r.text[:1500]); sys.exit(1)
    return r.json()

# 1. cover image
if "cover" not in state:
    with open("build/generative-ai-cover.jpg", "rb") as f:
        d = check(c.post("/api/media", files={"file": ("generative-ai-cover.jpg", f, "image/jpeg")},
                         data={"_payload": json.dumps({"alt": "Generative AI for Beginners course cover"})}))
    state["cover"] = d["doc"]["id"]; save()
print("cover", state["cover"])

# 2. course (draft)
if "course" not in state:
    body = {
        "title": "Generative AI for Beginners: Understand It, Use It, Build With It",
        "slug": "generative-ai-for-beginners",
        "status": "draft",
        "featured": False,
        "summary": "Learn what generative AI is, how to use it safely and well, and how to build small AI apps in Python with free models that run on your own computer.",
        "description": open("description.html").read(),
        "coverImage": state["cover"],
        "category": 4,
        "level": "beginner",
        "instructorName": "Avro Academy Team",
        "delivery": "self-paced",
        "access": "open",
        "sequential": False,
        "certificateEnabled": True,
        "meta": {"title": "Generative AI for Beginners: Free Course",
                 "description": "Free course: how generative AI works, using it responsibly, prompting, and building AI apps in Python with free local models. Certificate included."},
    }
    d = check(c.post("/api/courses", json=body))
    state["course"] = d["doc"]["id"]; save()
course = state["course"]
print("course", course)

# 3. downloads
files = {"zip": ("build/Generative-AI-Starter-Files.zip", "application/zip", "Generative AI starter files (ZIP)"),
         "pdf": ("build/Generative-AI-Cheat-Sheet.pdf", "application/pdf", "Generative AI cheat sheet (PDF)")}
for key, (path, mime, title) in files.items():
    if key not in state:
        with open(path, "rb") as f:
            d = check(c.post("/api/course-files", files={"file": (os.path.basename(path), f, mime)},
                             data={"_payload": json.dumps({"title": title, "course": course})}))
        state[key] = {"id": d["doc"]["id"], "filename": d["doc"]["filename"]}; save()
    print(key, state[key])

# 4. lessons + quizzes
m = json.load(open("manifest.json"))
state.setdefault("lessons", {})
def quiz(n):
    qs = []
    for q in json.load(open(f"quizzes/q{n}.json")):
        qs.append({"question": q["q"], "multiple": bool(q.get("multi")), "explanation": q["exp"],
                   "options": [{"text": t, "correct": bool(ok)} for t, ok in q["o"]]})
    return {"passMark": 70, "maxAttempts": 0, "showAnswers": True, "questions": qs}

ATTACH = {"1-4": ["zip", "pdf"], "2-3": ["zip"], "8-4": ["pdf"]}
curriculum = []
for n, mod in enumerate(m["modules"], start=1):
    ids = []
    for key, title, minutes, preview in mod["lessons"]:
        if key not in state["lessons"]:
            slug = title.lower()
            slug = "".join(ch if ch.isalnum() else "-" for ch in slug)
            slug = "-".join(p for p in slug.split("-") if p)[:80].strip("-")
            body = {"title": title, "course": course, "type": "text", "durationMinutes": minutes,
                    "slug": slug, "freePreview": preview, "body": open(f"lessons/{key}.html").read(),
                    "attachments": [state[a]["id"] for a in ATTACH.get(key, [])]}
            d = check(c.post("/api/course-lessons", json=body))
            state["lessons"][key] = d["doc"]["id"]; save()
        ids.append(state["lessons"][key])
    qkey = f"q{n}"
    if qkey not in state["lessons"]:
        title = "Final quiz" if n == 8 else f"Module {n} quiz"
        body = {"title": title, "course": course, "type": "quiz", "durationMinutes": 5,
                "slug": "final-quiz" if n == 8 else f"module-{n}-quiz", "freePreview": False,
                "body": "<p>Answer the questions below. You need 70% to pass, and you can try as many times as you like.</p>",
                "quiz": quiz(n)}
        d = check(c.post("/api/course-lessons", json=body))
        state["lessons"][qkey] = d["doc"]["id"]; save()
    ids.append(state["lessons"][qkey])
    curriculum.append({"title": mod["title"], "description": mod["description"], "lessons": ids})

# 5. curriculum (course stays draft)
d = check(c.patch(f"/api/courses/{course}", json={"curriculum": curriculum, "status": "draft"}))
print("curriculum set; status:", d["doc"]["status"], "sections:", len(d["doc"]["curriculum"]))
