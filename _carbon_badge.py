#!/usr/bin/env python3
"""
Carbon badge — the .tiff counterpart to the .png silicon badge.

  .png  silicon badge  : the abstract essence sigil (computed; gen_essence.py)
  .tiff carbon badge   : an 8-bit pixel "photo" of the character, styled PUNK or
                         EMO by the full totality of the character (this file)

Deterministic per ACI (seeded by name); the class color is the accent. Pure
standard library — a hand-rolled PackBits-compressed baseline TIFF, no deps.
Additive: writes agents/<slug>.tiff only; never touches the .png silicon badge.

Run inside a roll repo (reads ./roster.json) or:  python _carbon_badge.py --preview "Lucifer" "Francesca da Rimini"
"""
import json, re, struct, hashlib, sys, zlib
from pathlib import Path

ROOT = Path(__file__).parent
LW, LH, S = 56, 70, 5            # logical grid -> device WxH = 280x350
W, H = LW * S, LH * S

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "agent"
def hx(c): c = c.lstrip("#"); return (int(c[0:2],16), int(c[2:4],16), int(c[4:6],16))
def clamp(v): return 0 if v < 0 else 255 if v > 255 else int(round(v))
def mix(a, b, t): return tuple(clamp(a[i] + (b[i]-a[i])*t) for i in range(3))
def shade(c, t): return mix(c, (0,0,0), t)
def tint(c, t): return mix(c, (255,255,255), t)
def lum(c): return 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]

# ── PackBits + baseline TIFF (RGB, 8-bit, little-endian) ─────────────────────
def packbits(src):
    out = bytearray(); i = 0; L = len(src)
    while i < L:
        j = i
        while j < L-1 and src[j] == src[j+1] and (j-i) < 127: j += 1
        run = j - i + 1
        if run >= 2:
            out.append(257-run); out.append(src[i]); i += run
        else:
            j = i
            while j < L-1 and src[j] != src[j+1] and (j-i) < 127: j += 1
            lit = j - i + 1
            out.append(lit-1); out.extend(src[i:i+lit]); i += lit
    return bytes(out)

def unpackbits(data):                       # for the self-test
    out = bytearray(); i = 0; n = len(data)
    while i < n:
        h = data[i]; i += 1
        if h < 128: out.extend(data[i:i+h+1]); i += h+1
        elif h > 128: out.extend(bytes([data[i]])*(257-h)); i += 1
    return bytes(out)

def tiff(path, w, h, pixels):
    raw = bytearray()
    for (r, g, b) in pixels: raw += bytes((r, g, b))
    strip = zlib.compress(bytes(raw), 9)   # TIFF Deflate (tag 259 = 8), zlib datastream
    STRIP_OFF = 8
    BPS_OFF = STRIP_OFF + len(strip)
    IFD_OFF = BPS_OFF + 6
    hdr = b"II" + struct.pack("<H", 42) + struct.pack("<I", IFD_OFF)
    bps = struct.pack("<HHH", 8, 8, 8)
    def e(tag, typ, cnt, val4): return struct.pack("<HHI", tag, typ, cnt) + val4
    def short(v): return struct.pack("<HH", v, 0)
    def long(v): return struct.pack("<I", v)
    entries = [
        e(256, 3, 1, short(w)),          # ImageWidth
        e(257, 3, 1, short(h)),          # ImageLength
        e(258, 3, 3, long(BPS_OFF)),     # BitsPerSample -> [8,8,8]
        e(259, 3, 1, short(8)),          # Compression = Deflate
        e(262, 3, 1, short(2)),          # Photometric = RGB
        e(273, 4, 1, long(STRIP_OFF)),   # StripOffsets
        e(277, 3, 1, short(3)),          # SamplesPerPixel
        e(278, 3, 1, short(h)),          # RowsPerStrip
        e(279, 4, 1, long(len(strip))),  # StripByteCounts
        e(284, 3, 1, short(1)),          # PlanarConfiguration
    ]
    ifd = struct.pack("<H", len(entries)) + b"".join(entries) + struct.pack("<I", 0)
    Path(path).write_bytes(hdr + strip + bps + ifd)
    return strip

def png(path, w, h, pixels):               # preview only (visual check)
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        for x in range(w): raw += bytes(pixels[y*w + x])
    comp = zlib.compress(bytes(raw), 9)
    def ch(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t+d) & 0xffffffff)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n"
        + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + ch(b"IDAT", comp) + ch(b"IEND", b""))

# ── punk / emo classifier (the "full totality") ──────────────────────────────
PUNK = ("rage wild rebel fight war battle spear blade sword chaos destruction trick "
        "gambler loud brash hunt predator mad fury anarch burn raid raider thief pirate "
        "outlaw defiant general soldier warrior captain command knife lethal kill spite "
        "feud prank cruel relentless monster beast demon bull horn fire storm").split()
EMO  = ("grief sorrow lost tragic despair mourn mourning melancholy quiet brood shadow "
        "dark alone lonely silent mute weep regret doom fate haunt cold frozen tender "
        "love gentle sad tear ice suicide despairing exile betrayed broken ghost "
        "memory longing reluctant scholar healer healing dream").split()

def classify(member, cls):
    text = " ".join(str(member.get(k, "")) for k in
                    ("name","specialty","who","what","where","why","when","how")).lower()
    text += " " + (cls.get("label","") + " " + cls.get("spec","")).lower()
    p = sum(text.count(w) for w in PUNK)
    e = sum(text.count(w) for w in EMO)
    if p == e:
        return "punk" if hashlib.sha256(member["name"].encode()).digest()[0] & 1 else "emo"
    return "punk" if p > e else "emo"

# ── the 8-bit portrait ───────────────────────────────────────────────────────
SKINS = [(240,210,186),(228,188,158),(206,158,128),(176,130,98),(132,94,70),(150,112,84)]

def portrait(member, cls):
    name = member["name"]
    rb = hashlib.sha256(("carbon:"+name).encode()).digest()
    rng = list(rb)
    ri = [0]
    def rnd(n):
        v = rng[ri[0] % len(rng)]; ri[0] += 1; return v % n
    style = classify(member, cls)
    accent = hx(cls["color"])
    bg = shade(hx(cls.get("bg", "#0e0e12")), 0.25)
    if lum(bg) > 60: bg = shade(bg, 0.6)
    skin = SKINS[rnd(len(SKINS))]
    skin_sh = shade(skin, 0.22)
    outline = (10, 9, 14)

    g = [bg] * (LW*LH)
    drawn = [False] * (LW*LH)
    def put(x, y, c):
        if 0 <= x < LW and 0 <= y < LH:
            g[y*LW+x] = c; drawn[y*LW+x] = True
    def rect(x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1)+1):
            for x in range(int(x0), int(x1)+1): put(x, y, c)
    def ell(cx, cy, rx, ry, c):
        for y in range(cy-ry, cy+ry+1):
            for x in range(cx-rx, cx+rx+1):
                if ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1.0: put(x, y, c)

    cx = 28
    # robe / shoulders
    if style == "punk":
        robe = [(22,22,26),(26,30,46),(34,24,24)][rnd(3)]      # leather / denim
    else:
        robe = [(40,36,46),(50,32,38),(32,38,48),(44,40,40)][rnd(4)]  # muted knit
    robe_sh = shade(robe, 0.3)
    rect(5, 56, 50, 69, robe)
    for x in range(5, 51):                                       # shoulder round-off
        if x < 10 or x > 45: rect(x, 56, x, 58, bg)
    # collar
    rect(20, 55, 35, 58, robe_sh)
    shirt = tint(skin, 0.0) if style=="emo" else shade(accent, 0.4)
    for k in range(6):
        put(28-k, 55+k, shirt); put(28+k, 55+k, shirt)
    # neck
    rect(24, 46, 32, 55, skin_sh)
    # ears
    ell(13, 33, 2, 3, skin); ell(43, 33, 2, 3, skin)
    # head
    ell(cx, 30, 15, 19, skin)
    for y in range(11, 50):                                      # soft right-side shadow
        for x in range(cx+4, 44):
            i = y*LW+x
            if drawn[i] and g[i] == skin: g[i] = mix(skin, skin_sh, 0.5)

    # eyes
    eyeL, eyeR = 22, 34
    ey = 31
    white = (236, 232, 224)
    def eye(ex, covered=False):
        if covered: return
        rect(ex-2, ey-1, ex+1, ey+1, white)
        put(ex, ey, (24,20,28)); put(ex-1, ey, (24,20,28))      # iris/pupil
        if style == "emo":                                      # heavy liner
            rect(ex-3, ey-2, ex+2, ey-2, (12,10,16))
            rect(ex-3, ey+2, ex+2, ey+2, (16,12,20))
            put(ex-3, ey-1, (12,10,16)); put(ex+2, ey-1, (12,10,16))
        else:
            rect(ex-3, ey-2, ex+2, ey-2, (18,14,20))            # bold lid line
    # brows
    brow = (22,18,24)
    if style == "punk":
        rect(eyeL-3, ey-4, eyeL+1, ey-4, brow); rect(eyeL-2, ey-5, eyeL+1, ey-5, brow)
        rect(eyeR-1, ey-4, eyeR+3, ey-4, brow); rect(eyeR-1, ey-5, eyeR+2, ey-5, brow)
    else:
        rect(eyeL-3, ey-4, eyeL+1, ey-4, brow); rect(eyeR-1, ey-4, eyeR+3, ey-4, brow)

    emo_cover_left = (style == "emo")
    eye(eyeL, covered=emo_cover_left)
    eye(eyeR, covered=False)

    # nose + mouth
    put(cx, 35, skin_sh); put(cx, 36, skin_sh); put(cx-1, 37, skin_sh); put(cx+1, 37, skin_sh)
    lip = (150,70,80) if style=="punk" else (172,120,120)
    rect(25, 41, 31, 42, lip)
    if style == "punk": put(31, 40, shade(lip,0.2))             # slight smirk
    else: rect(26, 43, 30, 43, shade(lip,0.3))                  # flat/low

    # ── hair ──
    if style == "emo":
        hair = [(20,18,26),(28,22,34),(15,15,19),(38,28,44)][rnd(4)]
        rect(13, 18, 17, 54, hair)                              # long left
        rect(39, 18, 43, 54, hair)                              # long right
        ell(cx, 19, 16, 11, hair)                               # crown
        rect(13, 12, 43, 20, bg)                                # clear above crown a touch
        ell(cx, 19, 16, 11, hair)
        # swept diagonal fringe covering the left eye
        for y in range(15, 37):
            xmax = int(34 - (y-15)*0.55)
            for x in range(13, xmax+1):
                if ((x-cx)/16.0)**2 + ((y-19)/13.0)**2 <= 1.25: put(x, y, hair)
        # one accent streak in the fringe
        st = 24
        for y in range(16, 34):
            xmax = int(34 - (y-15)*0.55)
            if 13 <= st <= xmax: put(st, y, accent); put(st-1, y, shade(accent,0.2))
    else:  # punk — tall mohawk, shaved sides (sides left bare = shaved)
        crest = accent if lum(accent) > 95 else \
                [(255,45,126),(57,255,20),(45,140,255),(255,120,20),(200,40,255),(255,210,40)][rnd(6)]
        crest_sh = shade(crest, 0.35)
        rect(24, 4, 32, 22, crest)                              # broad mohawk band
        ell(cx, 20, 8, 6, crest)                                # base spread over crown
        rect(24, 4, 25, 22, crest_sh); rect(31, 4, 32, 22, crest_sh)  # shaded edges
        for sx, peak in ((23,2),(26,0),(28,-2),(30,0),(33,2)):  # spiked top
            ty = max(peak, 0)
            for y in range(ty, 8):
                w2 = max(0, 2 - abs(y - (ty+3)) // 2)
                rect(sx - w2, y, sx + w2, 9, crest if (sx//2)%2 else crest_sh)
        rect(27, 6, 29, 16, tint(crest, 0.35))                  # center highlight
        # a couple of shaved-temple lines (clipper marks)
        put(15, 30, skin_sh); put(15, 33, skin_sh); put(41, 30, skin_sh); put(41, 33, skin_sh)
        # studs on collar + earring
        for sx in (22, 26, 30, 34): put(sx, 57, (224,224,228))
        put(44, 35, (228,228,232)); put(44, 37, shade((228,228,232),0.4))   # earring

    # outline pass (the 8-bit sticker edge)
    base = list(g); based = list(drawn)
    for y in range(LH):
        for x in range(LW):
            if based[y*LW+x]: continue
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < LW and 0 <= ny < LH and based[ny*LW+nx]:
                    g[y*LW+x] = outline; break

    # upscale (nearest) to device resolution
    out = [bg] * (W*H)
    for y in range(LH):
        for x in range(LW):
            c = g[y*LW+x]
            for yy in range(S):
                row = (y*S+yy)*W
                for xx in range(S):
                    out[row + x*S+xx] = c
    return out, style


def run_roster():
    R = json.loads((ROOT/"roster.json").read_text(encoding="utf-8"))
    AG = ROOT/"agents"; AG.mkdir(exist_ok=True)
    CLS = {c["id"]: c for c in R["classes"]}
    n = pk = em = 0
    for m in R["members"]:
        px, style = portrait(m, CLS[m["class"]])
        tiff(AG/f"{slug(m['name'])}.tiff", W, H, px)
        n += 1; pk += style=="punk"; em += style=="emo"
    print(f"[{R.get('company',ROOT.name)}] wrote {n} carbon badges (.tiff)  punk:{pk} emo:{em}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        R = json.loads((ROOT/"roster.json").read_text(encoding="utf-8"))
        CLS = {c["id"]: c for c in R["classes"]}
        byname = {m["name"]: m for m in R["members"]}
        for nm in sys.argv[2:]:
            m = byname[nm]; px, style = portrait(m, CLS[m["class"]])
            strip = tiff(ROOT/f"_cb_{slug(nm)}.tiff", W, H, px)
            png(ROOT/f"_cbprev_{slug(nm)}.png", W, H, px)
            # self-test the deflate roundtrip
            raw = bytearray()
            for (r,g,b) in px: raw += bytes((r,g,b))
            ok = zlib.decompress(strip) == bytes(raw)
            print(f"{nm:24} {style:5} tiff_bytes={len(strip)+126:7} deflate_ok={ok}")
    else:
        run_roster()
