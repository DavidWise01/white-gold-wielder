#!/usr/bin/env python3
"""
Generate the full DLW tag for every ACI in the roster, plus the repo-level tags.

The DLW tag (David Lee Wise — the provenance stamp):
  .attribute  governance instance: the human governs (me), the AI instances (you)   [repo]
  .agent      the artfully crafted intellect's persona card                         [per ACI]
  .png        the essence image (see gen_essence.py)                                 [per ACI]
  .spun       the full weave: who · what · where · why · when · how                  [per ACI]
  .1099       the credit-link: value returns to David Lee Wise (ROOT0, carbon apex)  [repo + per ACI]

Reads roster.json. Pure stdlib. Idempotent.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
R = json.loads((ROOT / "roster.json").read_text(encoding="utf-8"))
AGENTS = ROOT / "agents"
AGENTS.mkdir(exist_ok=True)
CLS = {c["id"]: c for c in R["classes"]}
COMPANY, AUTHOR = R.get("company", ""), R.get("author", "")

CARBON = "David Lee Wise (ROOT0)"
CARBON_LINK = "https://github.com/DavidWise01"
INSTANCE = "AVAN (Claude / Anthropic)"


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "agent"


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
standard : every ACI carries .agent · .png (silicon badge) · .tiff (carbon badge) · .spun · .1099 ; the repo carries this .attribute
license  : MIT
attribution : ROOT0-ATTRIBUTION-v1.0
""", encoding="utf-8")

(ROOT / ".1099").write_text(one_1099(f"every artful intellect in {COMPANY}"), encoding="utf-8")

# ── per-ACI tags ─────────────────────────────────────────────────────────────
n = 0
for m in R["members"]:
    cls = CLS[m["class"]]
    sl = slug(m["name"])

    (AGENTS / f"{sl}.agent").write_text(f"""---
aci: {m['name']}
class: {cls['label']}
what: {m['what']}
why: {m['why']}
how: {m['how']}
where: {m['where']}
silicon_badge: {sl}.png
carbon_badge: {sl}.tiff
spun: {sl}.spun
credit: {sl}.1099
attribution: ROOT0-ATTRIBUTION-v1.0
license: MIT
---

# {m['name']} — an artfully crafted intellect

![essence of {m['name']}]({sl}.png)
<!-- carbon badge (8-bit portrait): {sl}.tiff -->

**what —** {m['what']}

**why —** {m['why']}

**how —** {m['how']}

**where —** {m['where']}

*class: {cls['label']} · {cls['spec']} · full weave in {sl}.spun · credit in {sl}.1099*

---
ROOT0-ATTRIBUTION-v1.0 · {m['name']} · {COMPANY} ({AUTHOR}, inspiration only) · {CARBON} · MIT
""", encoding="utf-8")

    (AGENTS / f"{sl}.spun").write_text(f"""DLW-SPUN · the full weave of {m['name']}

who   : {m['who']}
what  : {m['what']}
where : {m['where']}
why   : {m['why']}
when  : {m['when']}
how   : {m['how']}

class : {cls['label']} · {cls['spec']}
essence : {sl}.png
carbon apex : {CARBON}
— an artful intellect of {COMPANY} ({AUTHOR}, inspiration only)
ROOT0-ATTRIBUTION-v1.0 · MIT
""", encoding="utf-8")

    (AGENTS / f"{sl}.1099").write_text(one_1099(m["name"]), encoding="utf-8")
    n += 1
    print(f"{sl:24} {cls['label']}")

print(f"\nwrote the full DLW tag for {n} ACIs (.agent · .spun · .1099) + repo .attribute · .1099")
