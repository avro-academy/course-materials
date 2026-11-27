"""A lesson-plan generator: a prompt template filled in from what the tutor types."""
import ollama

MODEL = "llama3.2"

TEMPLATE = """You are helping a tutor at Brightside Tutoring plan a lesson.

Write a lesson plan for a {minutes}-minute small-group lesson.
Subject: {subject}
Year level: {year}
Topic: {topic}

Use exactly these headings: Goal, Warm-up, Teach, Practice, Exit question, Homework.
Give times in minutes for Warm-up, Teach and Practice, adding up to {minutes} minutes or less.
Keep the whole plan under 200 words. Use Australian spelling."""

subject = input("Subject: ")
year = input("Year level: ")
topic = input("Topic: ")
minutes = input("Lesson length in minutes [60]: ") or "60"

prompt = TEMPLATE.format(subject=subject, year=year, topic=topic, minutes=minutes)

stream = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}],
                     options={"temperature": 0.4}, stream=True)
print()
for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
print()
