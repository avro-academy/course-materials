"""Workplace quiz game — Python Foundations, Module 8.

Follow the steps in the lesson "Project: workplace quiz game".
Run it with:  python quiz.py   (or paste it into a Colab cell)
Stuck? Compare with quiz_finished.py.
"""
import random

# Step 1: the questions. "answer" is the number of the right option, starting at 1.
QUESTIONS = [
    {"question": "What does LAST stand for when handling a complaint?",
     "options": ["Listen, Apologise, Solve, Thank", "Laugh, Argue, Stop, Talk", "Leave, Ask, Say, Tell"],
     "answer": 1},
    # TODO: add at least three more questions
]


def ask(question):
    """Ask one question. Return True if the answer is right, otherwise False."""
    # Step 2:
    # 1. print the question
    # 2. print each option with its number (hint: enumerate(..., start=1))
    # 3. keep asking until the user types a valid number (hint: .isdigit())
    # 4. print "Correct!" and return True, or show the right answer and return False
    pass


def play():
    """Ask every question in a random order and print the score."""
    # Step 3: copy QUESTIONS, shuffle the copy, ask each one and count the right answers
    pass


if __name__ == "__main__":
    play()
