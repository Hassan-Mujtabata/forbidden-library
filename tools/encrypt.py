# -*- coding: utf-8 -*-
"""gzip + AES-256-GCM encrypt books.json -> ../content.enc; key -> key.txt (never committed)."""
import os, gzip, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "books.json")
DST = os.path.join(HERE, "..", "content.enc")
KEYFILE = os.path.join(HERE, "key.txt")

data = gzip.compress(open(SRC, "rb").read(), 9)

if os.path.exists(KEYFILE):  # reuse key so redeploys don't break the saved link
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
else:
    key = AESGCM.generate_key(256)
    open(KEYFILE, "w").write(base64.urlsafe_b64encode(key).decode().rstrip("="))

iv = os.urandom(12)
ct = AESGCM(key).encrypt(iv, data, None)
open(DST, "wb").write(iv + ct)

print(f"plain {os.path.getsize(SRC)/1e6:.2f} MB -> gzip {len(data)/1e6:.2f} MB -> content.enc {os.path.getsize(DST)/1e6:.2f} MB")
print("key: " + open(KEYFILE).read().strip())
