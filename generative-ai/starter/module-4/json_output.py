"""Get an answer your program can use: JSON that matches a schema."""
import json

import ollama

MODEL = "llama3.2"

schema = {
    "type": "object",
    "properties": {
        "student_name": {"type": "string"},
        "year_level": {"type": "integer"},
        "subject": {"type": "string", "enum": ["maths", "english", "science"]},
        "preferred_day": {"type": "string"},
    },
    "required": ["student_name", "year_level", "subject", "preferred_day"],
}

message = ("Hi, my son Leo is in Year 8 and really struggling with algebra. "
           "Wednesdays after school would suit us best. Thanks, Anna")

reply = ollama.chat(
    model=MODEL,
    messages=[{"role": "user", "content": "Pull the enrolment details out of this message:\n\n" + message}],
    format=schema,
    options={"temperature": 0},
)

enquiry = json.loads(reply["message"]["content"])
print(enquiry)
print(f"New {enquiry['subject']} enquiry for {enquiry['student_name']} (Year {enquiry['year_level']})")
