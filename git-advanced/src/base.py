from gh import *
R1='# Pay calculator\n\nWorks out pay for a shift.\n'
P1='BASE_RATE = 25.0\n\n\ndef shift_pay(hours, day):\n    return hours * BASE_RATE\n'
P2='BASE_RATE = 25.0\nWEEKEND = {"Saturday": 1.25, "Sunday": 1.5}\n\n\ndef shift_pay(hours, day):\n    return hours * BASE_RATE * WEEKEND.get(day, 1)\n'
HDR='import sys\nsys.dont_write_bytecode = True   # always test the current pay.py, never a cached copy\n\nfrom pay import shift_pay\n\n# Run with:  python test_pay.py   (prints OK, or stops with an error)\n'
T1=HDR+'assert shift_pay(4, "Monday") == 100.0\nassert shift_pay(0, "Monday") == 0\nprint("OK")\n'
T2=HDR+'assert shift_pay(4, "Monday") == 100.0\nassert shift_pay(4, "Saturday") == 125.0\nassert shift_pay(4, "Sunday") == 150.0\nassert shift_pay(0, "Monday") == 0\nprint("OK")\n'
GI='__pycache__/\n.env\n'
C1='4c070e5aeb024f46f04b24efdddb9d486d909a8d'
C2='560800fbfa869f52b670f205e876ca4543f2d022'
C3='17841d0'; C5='c910cf0cbd124faa556ae57da4d49b857b56ffa6'
P3=P2.replace('day):\n','day):\n    """Pay for one shift, before tax."""\n',1)
P4=P3.replace('"Sunday"','"sunday"')
P5=P4.replace('tax."""\n','tax."""\n    if hours < 0:\n        raise ValueError("hours can\'t be negative")\n')
R2='# Pay calculator\n\nWorks out pay for a shift, including weekend rates.\n'
R3=R2+'\nExample rates only — real rates depend on the award.\n'
CON='# Contributing\n\nRun `python test_pay.py` before opening a pull request.\n'
