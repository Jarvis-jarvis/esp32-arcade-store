#!/usr/bin/env python3
"""
Builds catalog.json from the games/ folder.

Every game is a folder:   games/<id>/index.html   (one self-contained file)
                          games/<id>/info.json    {"title","desc","icon","c1","c2","ver"}

Run this after adding or changing a game, then publish the folder (e.g. push to GitHub Pages).
Raise "ver" in info.json when you change a game so users see "Update".
"""
import hashlib, json, os, re, sys

root = os.path.dirname(os.path.abspath(__file__))
games_dir = os.path.join(root, "games")
games = []
for gid in sorted(os.listdir(games_dir)):
    d = os.path.join(games_dir, gid)
    if not os.path.isdir(d):
        continue
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,32}", gid):
        sys.exit("Bad game id (letters, numbers, - and _ only, max 32): " + gid)
    html = os.path.join(d, "index.html")
    infop = os.path.join(d, "info.json")
    if not (os.path.isfile(html) and os.path.isfile(infop)):
        print("skipping %s (needs index.html and info.json)" % gid)
        continue
    with open(infop, encoding="utf-8") as f:
        info = json.load(f)
    data = open(html, "rb").read()
    if len(data) > 300 * 1024:
        sys.exit("%s/index.html is bigger than 300 KB" % gid)
    games.append({
        "id": gid,
        "title": info.get("title", gid),
        "desc": info.get("desc", ""),
        "icon": info.get("icon", "🎮"),
        "c1": info.get("c1", "#00e5ff"),
        "c2": info.get("c2", "#ff2e88"),
        "ver": int(info.get("ver", 1)),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    })

with open(os.path.join(root, "catalog.json"), "w", encoding="utf-8") as f:
    json.dump({"games": games}, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("catalog.json written with %d game(s)" % len(games))
