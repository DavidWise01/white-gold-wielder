# -*- coding: utf-8 -*-
import json, io

PATH = r"C:\repos\white-gold-wielder\roster.json"

with io.open(PATH, "r", encoding="utf-8") as f:
    R = json.load(f)

# Six-W enrichments, grounded in each member's existing `specialty`
# and well-established Thomas Covenant canon. Archetypal where unsure;
# the series' hardest material treated as archetype, not graphic detail.
FIELDS = {
    "Lord Mhoram": {
        "who": "High Lord of the Council of Lords at Revelstone, seer and teacher.",
        "what": "The steady moral heart of the First Chronicles' defenders of the Land.",
        "where": "Revelstone and the councils and battlefields of the war against the Despiser.",
        "why": "Because wisdom and compassion must refuse despair, even when the end seems certain.",
        "when": "Through the long siege and trials of the First Chronicles.",
        "how": "By insight, patience, and a courage that finds hope where others find only ruin."
    },
    "Saltheart Foamfollower": {
        "who": "A Giant of Seareach, storyteller, and Covenant's truest friend.",
        "what": "The purest love in the Chronicles, given wholly to the Land.",
        "where": "From the homes of the Giants to the deepest places of Covenant's final ordeal.",
        "why": "Because friendship and the joy of story are worth any sacrifice.",
        "when": "Across the First Chronicles, to its culminating fire.",
        "how": "Through joy, laughter, and the caamora — giving himself to the fire so the Land might live."
    },
    "Pitchwife": {
        "who": "A Giant of the Search, deformed in body and gentle in spirit.",
        "what": "The mender and singer who keeps the Search whole in heart and hull.",
        "where": "Aboard Starfare's Gust and across the seas of the Second Chronicles.",
        "why": "For love of Gossamer Glowlimn and devotion to his companions.",
        "when": "Throughout the long voyage of the Giants' Search.",
        "how": "By singing cracked stone whole and answering hardship with humor and craft."
    },
    "The First of the Search": {
        "who": "Gossamer Glowlimn, Swordmain and leader of the Giants' Search.",
        "what": "The iron-willed commander who holds the Search to its long purpose.",
        "where": "At the head of the Search, from the Giants' homeland across distant waters.",
        "why": "To keep faith with an ancient charge and see the Land's peril met.",
        "when": "Through the seafaring quest of the Second Chronicles.",
        "how": "By honor, discipline, and a faith that endures every doubt."
    },
    "Sunder & Hollian": {
        "who": "A Graveler and an eh-Brand, ordinary folk of the Sunbane age.",
        "what": "The bearers who carry the Land's hope across a broken time.",
        "where": "Among the Stonedown and Woodhelven villages under the Sunbane.",
        "why": "Because even common people must shoulder the Land's future when the great are gone.",
        "when": "During the ravaged years of the Second Chronicles.",
        "how": "By the old village powers of stone and lianar, and stubborn human endurance."
    },
    "Stave": {
        "who": "A Haruchai cast out by the Masters for his choice.",
        "what": "Loyalty that outgrows the iron law of his own people.",
        "where": "At Linden Avery's side through the Last Chronicles.",
        "why": "Because he chooses Linden over the pride and judgment of the Masters.",
        "when": "Across the events of the Last Chronicles.",
        "how": "Through unflinching Haruchai strength tempered at last by humility."
    },
    "The Ranyhyn": {
        "who": "The great free horses of Ra.",
        "what": "Keepers of ancient promises no human could honor.",
        "where": "The plains of Ra and wherever their oaths call them across the Land.",
        "why": "To keep faith freely given, beyond compulsion or fear.",
        "when": "Across all the Chronicles, over centuries.",
        "how": "By pride, freedom, and the unbroken keeping of their word."
    },
    "Berek Halfhand": {
        "who": "The Lord-Fatherer of legend, founder of the line of Lords.",
        "what": "The headwaters of the lineage that shapes the Land's history.",
        "where": "In the ancient days at the root of the Land's age of Lords.",
        "why": "To answer ruin with the founding of Law and Earthpower.",
        "when": "In the deep past, the legend behind all that follows.",
        "how": "By forging the Staff of Law and the line of Lords from sacrifice."
    },
    "Linden Avery": {
        "who": "The Chosen, a physician who Sees the Land's health and sickness.",
        "what": "The one whose love both saves the Land and imperils it.",
        "where": "Throughout the Land of the Second and Last Chronicles, which are hers.",
        "why": "Out of a fierce love that will not let go of those she would heal.",
        "when": "Across the Second and Last Chronicles.",
        "how": "By her health-sense and, fatefully, by power turned to raising the dead and waking the Worm of the World's End."
    },
    "High Lord Elena": {
        "who": "Covenant and Lena's daughter, raised to High Lord.",
        "what": "Power bent to ruin with the best of intentions.",
        "where": "At Revelstone and in the forbidden reaches beyond the Law of Death.",
        "why": "Out of love and a vengeance she cannot master.",
        "when": "During the First Chronicles' war against the Despiser.",
        "how": "By breaking the Law of Death and so turning her own strength against the Land."
    },
    "Hile Troy": {
        "who": "A blind warmark from Covenant's world who can see only within the Land.",
        "what": "The commander who spends everything — at last his very self.",
        "where": "On the battlefields of the Land during the First Chronicles.",
        "why": "To win the war and prove worthy of the sight the Land grants him.",
        "when": "Across the campaigns of the First Chronicles, and beyond.",
        "how": "By absolute commitment to command, surrendering himself to become Caer-Caveral."
    },
    "The Haruchai": {
        "who": "The Bloodguard, and later the Masters of the Land.",
        "what": "Absolute devotion curdled into pride.",
        "where": "From their mountain home to their long watch over the Land.",
        "why": "To serve and guard by an unbending standard of their own making.",
        "when": "Across all three Chronicles.",
        "how": "Through their Vow and their rule — which do nearly as much harm as good."
    },
    "The Elohim": {
        "who": "Beautiful, amoral, self-regarding powers, the Würd of the Earth made flesh.",
        "what": "Aid and obstruction by lights no mortal can read.",
        "where": "In Elemesnedene and wherever their inscrutable concerns reach.",
        "why": "For purposes wholly their own, beyond mortal morality.",
        "when": "Chiefly in the Second and Last Chronicles.",
        "how": "By powers and designs that help and hinder in the same gesture."
    },
    "The Insequent": {
        "who": "The Mahdoubt, the Harrow, the Theomach — solitary masters of vast lore.",
        "what": "Bearers of immense knowledge, each serving only their own long purpose.",
        "where": "Wandering the margins of the Land, apart from its peoples.",
        "why": "Each for an aim entirely their own.",
        "when": "Through the Last Chronicles.",
        "how": "By singular, jealously held lore and cunning."
    },
    "Kevin Landwaster": {
        "who": "The High Lord whose despair broke the Land.",
        "what": "The cautionary grey at the root of all the Land's grief.",
        "where": "At Revelstone and across the Land he ruled.",
        "why": "Out of a despair the Despiser nursed and turned against him.",
        "when": "In the age before the First Chronicles, casting its shadow forward.",
        "how": "By loosing the Ritual of Desecration that laid the Land waste."
    },
    "Anele": {
        "who": "A blind, mad earth-seer, last of an old line.",
        "what": "A vessel through whom truth speaks and departs.",
        "where": "Wandering the Land of the Last Chronicles.",
        "why": "Driven by a burden of inheritance and loss he cannot set down.",
        "when": "Across the Last Chronicles.",
        "how": "By earth-sight and the way truth wears him like a borrowed coat and sets him down again."
    },
    "Esmer": {
        "who": "Cail's son, get of the merewives, grey made flesh.",
        "what": "Harm and help offered in the same breath.",
        "where": "At the edges of Linden's path through the Last Chronicles.",
        "why": "Torn forever between the loyalties and betrayals of his divided birth.",
        "when": "Throughout the Last Chronicles.",
        "how": "By aiding and betraying at once, unable to be wholly either."
    },
    "Thomas Covenant": {
        "who": "The white gold wielder — a leper exiled from his own world, the Unbeliever.",
        "what": "The anti-hero on whom everything turns, keystone of the Arch of Time.",
        "where": "Caught between his own world and the Land across all ten books.",
        "why": "Driven by guilt for an unforgivable act in the first days, and by a refusal to surrender.",
        "when": "From the First Chronicles to the Last Dark — the bound axis of the whole saga.",
        "how": "By wild magic answering his ring, and by the refusal to give it up that alone holds the Arch."
    },
    "Lord Foul the Despiser": {
        "who": "The bitterness at the heart of the world — Despiser, Corruption, Fangthane.",
        "what": "The Land's destroyer, and the dark proof of its meaning.",
        "where": "From his strongholds to every corner of the Land he would unmake.",
        "why": "To break the Arch of Time and be free of the world that binds him.",
        "when": "Behind every Chronicle, the bound center opposite the Wielder.",
        "how": "By whispering 'you are mine' — for he is Covenant's own despair given a voice."
    },
}

names_in_file = [m["name"] for m in R["members"]]
for m in R["members"]:
    nm = m["name"]
    if nm not in FIELDS:
        raise RuntimeError("Unmatched member (no six-W authored): %r" % nm)
    f6 = FIELDS[nm]
    for k in ("who", "what", "where", "why", "when", "how"):
        if k not in f6 or not isinstance(f6[k], str) or not f6[k].strip():
            raise RuntimeError("Member %r missing field %r" % (nm, k))
        m[k] = f6[k]

# Guard against stray authored names not present in file
for nm in FIELDS:
    if nm not in names_in_file:
        raise RuntimeError("Authored name not found in roster: %r" % nm)

# Append the note sentence
R["note"] = R["note"] + " Every ACI now carries the full DLW tag with an authored six-W .spun."

out = json.dumps(R, ensure_ascii=False, indent=2) + "\n"
with io.open(PATH, "w", encoding="utf-8") as f:
    f.write(out)

# Confirm re-parse
with io.open(PATH, "r", encoding="utf-8") as f:
    chk = json.load(f)
assert len(chk["members"]) == len(FIELDS)
for m in chk["members"]:
    for k in ("who", "what", "where", "why", "when", "how"):
        assert k in m and m[k].strip(), (m["name"], k)
print("Patched %d members; JSON re-parses OK." % len(chk["members"]))
