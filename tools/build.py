# -*- coding: utf-8 -*-
"""Validate the idea-graph, merge it with the library, gzip + AES-256-GCM encrypt -> ../content.enc."""
import os, json, gzip, base64, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HERE = os.path.dirname(os.path.abspath(__file__))
BOOKS = os.path.join(HERE, "books.json")
GRAPH = os.path.join(HERE, "graph.json")
DST = os.path.join(HERE, "..", "content.enc")
KEYFILE = os.path.join(HERE, "key.txt")


def die(msg):
    print("FAIL:", msg)
    sys.exit(1)


def validate(books, graph):
    tracks = {t["id"] for t in graph["tracks"]}
    nodes = graph["nodes"]
    ids = [n["id"] for n in nodes]
    if len(ids) != len(set(ids)):
        die("duplicate node ids")
    idset = set(ids)
    booktitles = {b["title"] for b in books["books"]}

    problems, warns = [], []
    for n in nodes:
        if n["track"] not in tracks:
            problems.append(f"{n['id']}: unknown track {n['track']}")
        for p in n.get("prereq", []):
            if p not in idset:
                problems.append(f"{n['id']}: prereq '{p}' does not exist")
        if not n.get("stub"):
            for key in ("bridge", "sources", "quiz", "apply"):
                if not n.get(key):
                    problems.append(f"{n['id']}: authored node missing '{key}'")
            for q in n.get("quiz", []):
                if not (0 <= q["a"] < len(q["c"])):
                    problems.append(f"{n['id']}: quiz answer index out of range")
            for s in n.get("sources", []):
                if s["book"] not in booktitles:
                    warns.append(f"{n['id']}: source '{s['book']}' not a library book (quarried/external — no cross-link)")

    # cycle detection (DFS)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in ids}
    pre = {n["id"]: n.get("prereq", []) for n in nodes}

    def dfs(u, stack):
        color[u] = GRAY
        for v in pre[u]:
            if color[v] == GRAY:
                die(f"cycle detected: {' -> '.join(stack + [u, v])}")
            if color[v] == WHITE:
                dfs(v, stack + [u])
        color[u] = BLACK

    for i in ids:
        if color[i] == WHITE:
            dfs(i, [])

    # reachability: every node's prereq chain bottoms out at a root (prereq == [])
    roots = [n["id"] for n in nodes if not n.get("prereq")]
    if not roots:
        die("no root nodes (every node has a prereq -> nothing is ever available)")

    if problems:
        for p in problems:
            print("  PROBLEM:", p)
        die(f"{len(problems)} structural problem(s)")

    return warns, roots


def load_graph():
    """#49: prefer local plaintext graph.json; if it's absent (it is no longer committed to the repo),
    derive the graph from the encrypted content.enc so a fresh clone with the key can still rebuild."""
    if os.path.exists(GRAPH):
        return json.load(open(GRAPH, encoding="utf-8"))
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    raw = open(DST, "rb").read()
    pt = AESGCM(key).decrypt(raw[:12], raw[12:], None)
    payload = json.loads(gzip.decompress(pt))
    return {"tracks": payload["tracks"], "nodes": payload["nodes"]}


def main():
    check_only = "--check" in sys.argv                     # #56: validate the graph without needing the key / writing output
    books = json.load(open(BOOKS, encoding="utf-8"))
    graph = load_graph()
    warns, roots = validate(books, graph)

    authored = [n for n in graph["nodes"] if not n.get("stub")]
    stubs = [n for n in graph["nodes"] if n.get("stub")]
    print(f"tracks={len(graph['tracks'])}  nodes={len(graph['nodes'])} "
          f"(authored={len(authored)}, stub={len(stubs)})  roots={roots}")
    print("integrity: acyclic OK, all prereqs resolve OK, roots present OK")
    for w in warns:
        print("  note:", w)

    if check_only:
        print("check-only: graph is valid; not writing content.enc")
        return

    payload = {"v": 2, "books": books["books"], "tracks": graph["tracks"], "nodes": graph["nodes"]}
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    data = gzip.compress(raw, 9)

    if not os.path.exists(KEYFILE):
        die("key.txt missing — run the original encrypt.py once or restore the key")
    key = base64.urlsafe_b64decode(open(KEYFILE).read().strip() + "==")
    iv = os.urandom(12)
    ct = AESGCM(key).encrypt(iv, data, None)
    open(DST, "wb").write(iv + ct)

    print(f"payload {len(raw)/1e6:.2f} MB -> gzip {len(data)/1e6:.2f} MB -> content.enc {os.path.getsize(DST)/1e6:.2f} MB")


if __name__ == "__main__":
    main()
