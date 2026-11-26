"""Builds ../build/Python-Foundations-Starter-Files/ and checks every solution runs."""
import json, os, shutil, subprocess, sys, tempfile
from tasks import MODULES, TASKS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'build', 'Python-Foundations-Starter-Files')
INPUTS = {(2, 4): "38.5\n25\n3\n4\n", (7, 2): "six\n-2\n7.5\n25\n"}


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.rstrip('\n').splitlines(True)}


def notebook(cells):
    return {"nbformat": 4, "nbformat_minor": 5, "cells": cells,
            "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"},
                         "language_info": {"name": "python"}, "colab": {"provenance": []}}}


def build_nb(solutions):
    title = "Python Foundations: solutions" if solutions else "Python Foundations: practice notebook"
    intro = (f"# {title}\n\nAvro Academy · Python Foundations: Your First Programs\n\n" +
             ("Worked solutions for every task. Try each task yourself first! There's often more than one right answer."
              if solutions else
              "Every **Try it** task from the course is here. Click a code cell, write your code, and press **Shift + Enter** to run it.\n\n"
              "- Run the cells in order: a variable made in one cell is only there once that cell has run.\n"
              "- Stuck? Read the error from the bottom up, then check `Python-Foundations-Solutions.ipynb`.\n"
              "- Colab: **File → Upload notebook** and choose this file."))
    cells = [md(intro)]
    for m, name in MODULES.items():
        cells.append(md(f"## Module {m}: {name}"))
        for (mm, n, t, ins, starter, sol) in TASKS:
            if mm != m:
                continue
            cells.append(md(f"### Task {n}: {t}\n\n{ins}"))
            cells.append(code(sol if solutions else starter))
    return notebook(cells)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='\n') as f:
        f.write(text)


def check():
    bad = 0
    with tempfile.TemporaryDirectory() as d:
        for (m, n, t, ins, starter, sol) in TASKS:
            for label, src in (('solution', sol), ('starter', starter)):
                r = subprocess.run([sys.executable, '-I', '-c', src], cwd=d, input=INPUTS.get((m, n), "1\n" * 8),
                                   capture_output=True, text=True, timeout=20)
                if r.returncode != 0:
                    bad += 1
                    print(f'FAIL {label} {m}.{n}', r.stderr[-400:])
    return bad


if os.path.exists(OUT):
    shutil.rmtree(OUT)
write(os.path.join(OUT, 'Python-Foundations-Practice.ipynb'), json.dumps(build_nb(False), indent=1, ensure_ascii=False))
write(os.path.join(OUT, 'Python-Foundations-Solutions.ipynb'), json.dumps(build_nb(True), indent=1, ensure_ascii=False))
for m, name in MODULES.items():
    ex = [f'# Module {m}: {name} — exercises\n# Write your code under each task, then run this file: python module{m}_exercises.py\n']
    so = [f'# Module {m}: {name} — solutions\n']
    for (mm, n, t, ins, starter, sol) in TASKS:
        if mm != m:
            continue
        comment = '\n'.join('# ' + l if l else '#' for l in ins.splitlines())
        ex.append(f'\n# ── Task {n}: {t} ' + '─' * max(4, 50 - len(t)) + f'\n{comment}\n\n{starter}')
        so.append(f'\n# ── Task {n}: {t} ' + '─' * max(4, 50 - len(t)) + f'\n\n{sol}')
    write(os.path.join(OUT, 'exercises', f'module{m}_exercises.py'), ''.join(ex))
    write(os.path.join(OUT, 'solutions', f'module{m}_solutions.py'), ''.join(so))
for p in ('quiz-game/quiz.py', 'quiz-game/quiz_finished.py', 'budget-tracker/budget.py', 'budget-tracker/budget_finished.py'):
    os.makedirs(os.path.join(OUT, 'projects', os.path.dirname(p)), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'projects', p), os.path.join(OUT, 'projects', p))
shutil.copy(os.path.join(HERE, 'README.txt'), os.path.join(OUT, 'README.txt'))
bad = check()
print('built', OUT, 'failures:', bad)
