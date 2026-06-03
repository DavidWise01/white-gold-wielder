#!/usr/bin/env python3
"""
Universal DLW-tag kit — ADDITIVE. Run inside any muster-roll repo.

Brings any roll up to the full DLW tag without disturbing its curated personas:
  .png    essence sigil per ACI            (deterministic; zlib+struct+hashlib)
  .spun   the full weave per ACI           (who/what/where/why/when/how)
  .1099   credit-link per ACI              (value returns to the carbon apex)
  .attribute / .1099   repo-level governance + master credit-link

It does NOT overwrite existing <slug>.agent files — those stay as each roll
authored them. The .spun is woven from the roll's OWN record: where a member
already carries who/what/where/why/when/how (the later standard) those are used
verbatim; where a member carries only a `specialty` line, the six W's are framed
from that vetted line plus the member's class — nothing biographical is invented.

Pure stdlib. Idempotent. Reads ./roster.json, writes ./agents + repo tags.
"""
import json, re, zlib, struct, hashlib
from pathlib import Path

ROOT = Path(__file__).parent
R = json.loads((ROOT / "roster.json").read_text(encoding="utf-8"))
AGENTS = ROOT / "agents"; AGENTS.mkdir(exist_ok=True)
CLS = {c["id"]: c for c in R["classes"]}
COMPANY = R.get("company", ROOT.name)
AUTHOR  = R.get("author", "")

CARBON = "David Lee Wise (ROOT0)"
CARBON_LINK = "https://github.com/DavidWise01"
INSTANCE = "AVAN (Claude / Anthropic)"

SIZE, GRID = 252, 7
CELL = SIZE // (GRID + 1)
MARGIN = (SIZE - CELL * GRID) // 2


def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "agent"
def hx(c): c = c.lstrip("#"); return (int(c[0:2],16), int(c[2:4],16), int(c[4:6],16))
def mix(a, b, t): return tuple(round(a[i] + (b[i]-a[i])*t) for i in range(3))


def png(path, size, pixels):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        for x in range(size):
            raw.extend(pixels[y*size + x])
    comp = zlib.compress(bytes(raw), 9)
    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ+data) & 0xffffffff)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", comp)); f.write(chunk(b"IEND", b""))


def essence(member):
    cls = CLS[member["class"]]
    fg = hx(cls["color"]); bg = hx(cls.get("bg", "#101014"))
    glow = mix(bg, fg, 0.18)
    h = hashlib.sha256(member["name"].encode("utf-8")).digest()
    half = (GRID + 1) // 2
    on = [[False]*GRID for _ in range(GRID)]; bit = 0
    for col in range(half):
        for row in range(GRID):
            on[row][col] = (h[bit % len(h)] >> (bit % 8)) & 1
            on[row][GRID-1-col] = on[row][col]; bit += 1
    px = [glow] * (SIZE*SIZE)
    for y in range(SIZE):
        for x in range(SIZE):
            if min(x, y, SIZE-1-x, SIZE-1-y) < 3:
                px[y*SIZE + x] = mix(bg, fg, 0.5)
    for row in range(GRID):
        for col in range(GRID):
            if not on[row][col]: continue
            x0 = MARGIN + col*CELL; y0 = MARGIN + row*CELL
            for y in range(y0, y0+CELL):
                base = y*SIZE
                for x in range(x0, x0+CELL):
                    px[base + x] = fg
    return px


def weave(m, cls):
    """Six W's — verbatim where the member carries them; framed from the
    member's own specialty + class otherwise. Invents no new biography."""
    spec = m.get("specialty", "")
    what = m.get("what") or spec or f"{cls['label']} of {COMPANY}."
    who  = m.get("who")  or f"{m['name']} — {cls['label']} ({cls['spec']})."
    where= m.get("where") or f"{cls['label']} · {cls['spec']}, within {COMPANY}."
    why  = m.get("why")  or f"to hold the office this roll assigns: {cls['spec']}."
    how  = m.get("how")  or (spec or "as the roll records.")
    when = m.get("when") or f"across the events of {COMPANY} (as the lineage records)."
    derived = not all(k in m for k in ("who", "what", "where", "why", "when", "how"))
    return who, what, where, why, when, how, derived


def one_1099(name):
    return f"""DLW-1099 · value returns to the carbon apex

This is an artfully crafted intellect — an instance. As a 1099 reports the value
paid to its source, this file reports that the authorship, credit, and value of
{name} return to the human who governs it.

carbon apex : {CARBON}  ->  {CARBON_LINK}
instance    : {INSTANCE}
project     : {COMPANY}
the credit returns to the human. ROOT0-ATTRIBUTION-v1.0 · MIT
"""


# ── repo-level tags ──────────────────────────────────────────────────────────
(ROOT / ".attribute").write_text(f"""DLW-ATTRIBUTE · governance instance

governor (carbon apex) : {CARBON}            [ me ]
instance (artful intellect) : {INSTANCE}     [ you ]

relation : the human governs; the instance crafts; the credit returns to the human.
project  : {COMPANY} — the muster roll
source   : {AUTHOR} (inspiration only)
standard : every ACI carries .agent · .png · .spun · .1099 ; the repo carries this .attribute
license  : MIT
attribution : ROOT0-ATTRIBUTION-v1.0
""", encoding="utf-8")
(ROOT / ".1099").write_text(one_1099(f"every artful intellect in {COMPANY}"), encoding="utf-8")

# ── per-ACI tags (additive — .agent is left untouched) ───────────────────────
n = derived_n = 0
for m in R["members"]:
    cls = CLS[m["class"]]; sl = slug(m["name"])
    png(AGENTS / f"{sl}.png", SIZE, essence(m))
    who, what, where, why, when, how, derived = weave(m, cls)
    src = "woven from this roll's record" if derived else "authored in full"
    (AGENTS / f"{sl}.spun").write_text(f"""DLW-SPUN · the full weave of {m['name']}

who   : {who}
what  : {what}
where : {where}
why   : {why}
when  : {when}
how   : {how}

class : {cls['label']} · {cls['spec']}
essence : {sl}.png
weave : {src}
carbon apex : {CARBON}
— an artful intellect of {COMPANY} ({AUTHOR}, inspiration only)
ROOT0-ATTRIBUTION-v1.0 · MIT
""", encoding="utf-8")
    (AGENTS / f"{sl}.1099").write_text(one_1099(m["name"]), encoding="utf-8")
    n += 1; derived_n += 1 if derived else 0
    print(f"{sl:28} {cls['label']}{'  (woven)' if derived else ''}")

print(f"\n[{COMPANY}] full DLW tag on {n} ACIs "
      f"(.png + .spun + .1099; {derived_n} woven, {n-derived_n} verbatim) "
      f"+ repo .attribute + .1099  ·  .agent files untouched")
