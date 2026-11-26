"""How authenticator apps make their 6-digit codes (TOTP), using only Python's standard library.

    python3 totp.py
"""
import base64
import hashlib
import hmac
import struct
import time

SECRET = "JBSWY3DPEHPK3PXP"   # made-up example secret — the app and the website both keep a copy (from the QR code)


def code(secret, at):
    counter = int(at // 30)                                   # which 30-second window we're in
    digest = hmac.new(base64.b32decode(secret), struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return f"{number % 1_000_000:06d}"


now = time.time()
print(f"Code now:              {code(SECRET, now)}   (changes in {30 - int(now) % 30} seconds)")
print(f"Code 30 seconds later: {code(SECRET, now + 30)}")
print(f"Code with a different secret: {code('KRSXG5CTMVRXEZLU', now)}")
