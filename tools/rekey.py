# -*- coding: utf-8 -*-
"""#99: emergency re-key. Use if the unlock link ever leaks.

Generates a fresh 256-bit key and re-encrypts content.enc and every queued job under it,
then writes the new key.txt and prints the new unlock fragment + the value to set for the
VAULT_KEY GitHub secret.

CONSEQUENCES (by design — a leaked key can't be un-leaked any other way):
  * The OLD unlock link stops working. Reopen the app with the NEW link below.
  * Cross-device sync gists were encrypted with the OLD key: on each device, sign in again
    and use "Restore backup" / re-sync once — progress isn't lost, it just needs re-wrapping.
  * Any Windows-Hello face-unlock enrolments must be re-enrolled (they wrapped the old key).

Run:  python tools/rekey.py --yes
"""
import os, sys, json, gzip, base64, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
KEYFILE = os.path.join(HERE, "key.txt")
CONTENT = os.path.join(HERE, "..", "content.enc")
QUEUE = os.path.join(HERE, "queue")


def load(k, path):
    raw = open(path, "rb").read()
    return gzip.decompress(AESGCM(k).decrypt(raw[:12], raw[12:], None))


def save(k, path, data):
    iv = os.urandom(12)
    open(path, "wb").write(iv + AESGCM(k).encrypt(iv, gzip.compress(data, 9), None))


def main():
    if "--yes" not in sys.argv:
        print("This re-encrypts the whole vault under a NEW key and invalidates the old link.")
        print("Re-read the header, then run again with --yes to proceed.")
        return
    old = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    new_raw = secrets.token_bytes(32)

    save(new_raw, CONTENT, load(old, CONTENT))
    n = 0
    if os.path.isdir(QUEUE):
        for f in os.listdir(QUEUE):
            if f.endswith(".job.enc"):
                p = os.path.join(QUEUE, f)
                save(new_raw, p, load(old, p)); n += 1

    new_b64 = base64.urlsafe_b64encode(new_raw).decode().rstrip("=")
    open(KEYFILE, "w").write(new_b64)
    print(f"Re-encrypted content.enc and {n} queued job(s) under the new key.")
    print("key.txt updated.")
    print("Set the GitHub secret VAULT_KEY to:", new_b64)
    print("Your NEW unlock fragment:  #k=" + new_b64)
    print("Commit the re-encrypted content.enc (and any queue files), then open the app with the new link.")


if __name__ == "__main__":
    main()
