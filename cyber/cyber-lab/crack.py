"""How fast do passwords fall? A 'dictionary attack' on some made-up staff password hashes — your own, on your own computer.

    python3 crack.py
"""
import hashlib
import time

# A badly built old system stored passwords as MD5 hashes. These are the (made-up) staff accounts.
STAFF = {"alex": "sunshine", "jo": "Coffee2026", "priya": "Melbourne1", "sam": "flat-white-every-day",
         "mel": "Kettle-Harbour-Violin-77"}
LEAKED = {name: hashlib.md5(pw.encode()).hexdigest() for name, pw in STAFF.items()}

print("What an attacker sees after a data breach:")
for name, h in LEAKED.items():
    print(f"  {name:6} {h}")


def guesses():
    """Common passwords, plus the tweaks people think are clever: Capital letters, years and numbers on the end."""
    for word in open("common-passwords.txt").read().split():
        for w in {word, word.capitalize()}:
            yield w
            for end in ["1", "123", "!", "2025", "2026"]:
                yield w + end


start, tries, found = time.time(), 0, {}
wanted = {h: name for name, h in LEAKED.items()}
for guess in guesses():
    tries += 1
    h = hashlib.md5(guess.encode()).hexdigest()
    if h in wanted:
        found[wanted[h]] = guess
print(f"\nTried {tries:,} guesses in {time.time() - start:.2f} seconds")
for name in STAFF:
    print(f"  {name:6} {'CRACKED: ' + found[name] if name in found else 'not cracked'}")

# Why the way passwords are stored matters: guesses per second for each kind of hash
print("\nGuesses per second on this computer:")
for label, fn in [("MD5 (fast — bad for passwords)", lambda p: hashlib.md5(p).digest()),
                  ("PBKDF2, 600,000 rounds (slow — good)", lambda p: hashlib.pbkdf2_hmac("sha256", p, b"salt", 600_000))]:
    n, t = 0, time.time()
    while time.time() - t < 1.5:
        fn(b"guess%d" % n); n += 1
    print(f"  {label:38} {n / (time.time() - t):>12,.0f}")
