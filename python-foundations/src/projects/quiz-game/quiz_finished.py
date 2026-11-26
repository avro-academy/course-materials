"""Workplace quiz game (finished version) — Python Foundations, Module 8."""
import random

QUESTIONS = [
    {"question": "What does LAST stand for when handling a complaint?",
     "options": ["Listen, Apologise, Solve, Thank", "Laugh, Argue, Stop, Talk", "Leave, Ask, Say, Tell"],
     "answer": 1},
    {"question": "Which is the strongest password?",
     "options": ["Password123", "Your pet's name", "Four random words"],
     "answer": 3},
    {"question": "A customer's card is declined. What should you do first?",
     "options": ["Tell everyone in the queue", "Quietly ask if they'd like to try another way to pay", "Refuse to serve them"],
     "answer": 2},
    {"question": "You're running late for a shift. When should you tell your manager?",
     "options": ["As soon as you know", "When you arrive", "Only if they ask"],
     "answer": 1},
    {"question": "What is 10% GST on a $20 item?",
     "options": ["$0.20", "$2.00", "$20.00"],
     "answer": 2},
]


def ask(question):
    """Ask one question. Return True if the answer is right."""
    print(question["question"])
    for number, option in enumerate(question["options"], start=1):
        print(f"  {number}. {option}")
    while True:
        choice = input("Your answer (number): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(question["options"]):
            break
        print(f"Please type a number from 1 to {len(question['options'])}.")
    if int(choice) == question["answer"]:
        print("Correct!\n")
        return True
    print(f"Not quite — the answer is: {question['options'][question['answer'] - 1]}\n")
    return False


def play():
    questions = QUESTIONS.copy()
    random.shuffle(questions)
    score = 0
    for question in questions:
        if ask(question):
            score += 1
    print(f"You scored {score} out of {len(questions)}.")
    if score == len(questions):
        print("Perfect score!")


if __name__ == "__main__":
    play()
