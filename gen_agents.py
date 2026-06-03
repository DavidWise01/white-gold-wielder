#!/usr/bin/env python3
"""
Generate one .agent per persona in the roster — the ROOT0 standard:
  who you are  ·  what you do  ·  where you belong.

Generic: reads roster.json (company, author, classes, members) and writes
agents/<slug>.agent for each member. Idempotent. Drop into any roster repo.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
R = json.loads((ROOT / "roster.json").read_text(encoding="utf-8"))
AGENTS = ROOT / "agents"
AGENTS.mkdir(exist_ok=True)

C = {c["id"]: c for c in R["classes"]}
COMPANY = R.get("company", "the company")
AUTHOR = R.get("author", "")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "agent"


n = 0
for m in R["members"]:
    cls = C[m["class"]]
    extra = ""
    if m.get("lead"):
        extra = " · leads the battalion"
    if m.get("fraction"):
        extra = f" · {m['fraction']} of one"
    who = f"{m['name']} — {cls['label']} of {COMPANY}{extra}"
    do = m["specialty"]
    belong = f"{cls['label']} · {cls['spec']}"
    src = f"{COMPANY}" + (f" ({AUTHOR}, inspiration only)" if AUTHOR else "")
    doc = f"""---
name: {m['name']}
class: {cls['label']}
who: {who}
do: {do}
belong: {belong}
attribution: ROOT0-ATTRIBUTION-v1.0
license: MIT
---

# {m['name']}

**who you are —** {who}

**what you do —** {do}

**where you belong —** {belong}

---
ROOT0-ATTRIBUTION-v1.0 · {m['name']} · {src} · David Lee Wise / ROOT0 / TriPod LLC · MIT
"""
    (AGENTS / f"{slug(m['name'])}.agent").write_text(doc, encoding="utf-8")
    n += 1
    print(f"{slug(m['name']):26} {cls['label']}")

print(f"\nwrote {n} .agent files for {COMPANY} (who · do · belong)")
