"""Build pph-zone3-spec.json from the measurement constants in the live index.html.
Usage: python make_spec.py <repo-dir>
The page is the authority: every length below is parsed from its `const` block, then
converted to inches and 10 px = 1 in canvas pixels. Statuses are carried from the page's own notes."""
import json, re, sys, os
repo = sys.argv[1]
html = open(os.path.join(repo, "index.html"), encoding="utf-8").read()

# --- parse the measurement block ---------------------------------------------------
blk = html[html.index("measurements (decimal feet)"): html.index("three setup")]
ft = lambda f, i=0: f + i / 12
env = {"ft": ft}
for stmt in re.findall(r"const ([^;]+);", blk):
    for part in re.split(r",(?![^()]*\))", stmt):          # split on commas outside parens
        m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)", part.strip())
        if not m: continue
        name, expr = m.groups()
        expr = re.sub(r"//.*$", "", expr).strip()
        if name in ("ft", "COLS_X") or "=>" in expr: continue
        try: env[name] = eval(expr, {"__builtins__": {}}, env)
        except Exception: pass
g = env
need = ["W","D","WALL1","L","H","STEP","BH_UNDER","BH_PROJ","B2_DOOR_W","B2_DOOR_H","B2_DOOR_RIGHT",
        "M4W","BAND","XMAX","M7W","M8W","M6W","EYE","rEnd","rStart","dEnd","dStart","lEnd","lStart","SILL","COL_D","COL_FAR",
        "TRIM","BASE","MIR_H","MIR_IN","MIR_OUT"]
missing = [k for k in need if k not in g]
assert not missing, f"could not parse {missing} from index.html"
w1 = re.search(r"const W1_D0=([\d.]+), W1_D1=ft\(([\d.]+),([\d.]+)\), W1_DH=ft\(([\d.]+),([\d.]+)\)", html)
W1_D0, W1_D1, W1_DH = float(w1[1]), ft(float(w1[2]), float(w1[3])), ft(float(w1[4]), float(w1[5]))
M8Y = g["D"] - g["M7W"]; BX = g["W"] + g["M6W"] + 8; BOXN = g["XMAX"] - g["M8W"]

# --- helpers -----------------------------------------------------------------------
PX = 10
inch = lambda f: f * 12
px = lambda f: int(round(inch(f) * PX))
def ftin(f):
    h = round(f * 24); F, r = divmod(h, 24)             # nearest half inch
    i = r / 2
    return f"{F} ft" + (f" {i:g} in" if i else "")
def canvas(wf, hf):
    return {"px": [px(wf), px(hf)], "ratio": round(inch(wf) / inch(hf), 3), "ratio_text": f"{inch(wf)/inch(hf):.3f} : 1"}
def dims(wf, hf, status):
    return {"length_in": round(inch(wf), 2), "length_text": ftin(wf), "height_in": round(inch(hf), 2), "height_text": ftin(hf),
            "status": status, "canvas": canvas(wf, hf)}
LIVE = "https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/"
W, D, L, H = g["W"], g["D"], g["L"], g["H"]
b2s0 = W - g["B2_DOOR_RIGHT"] - g["B2_DOOR_W"]           # from the Wall 1 corner, as the page computes it
walls = []

# --- bottom trim: its own layer on every wall, broken at doorways (with the casing), running under windows ---------
BASE, CAS = g["BASE"], g["TRIM"]
BASE_STATUS = ("PROVISIONAL, not taped: 8 in from Tripp's note on the 10-07 panorama. Other readings: 4 in taped on the "
               "Zone 4 hallway (M9 / C1) sheet; about 7 in read off the M7 photo. One constant (BASE) in index.html.")
fid = lambda wid: wid.replace("+", "-")                   # file id: + becomes -
def base_trim(wid, wf, gaps=(), note=None):
    runs, a = [], 0.0
    for s0, s1 in sorted(gaps):
        if s0 > a: runs.append([px(a), px(s0)])
        a = max(a, s1)
    if wf > a: runs.append([px(a), px(wf)])
    k = {"what": f"bottom trim, white, {round(inch(BASE))} in high, not paintable. Its own layer over the photo and the design.",
         "from_floor_px": [0, px(BASE)], "runs_x_px": runs, "layer": f"layers/trim/{fid(wid)}.png", "status": BASE_STATUS}
    if note: k["note"] = note
    return k

walls.append({"wall": 1, "id": "Wall1", "aliases": ["B2.5", "Box side wall"], "name": "Box side wall, left of B2. No band, no art.", "art": False,
  **dims(g["WALL1"], L, "measured 19 ft 2 in; the same figure also appears as the column-to-M4 gap, one laser shot of Wall 1 settles it"),
  "tex": "tex/Wall1.jpg",
  "keepouts": [{"what": "doorway", "x_px": [px(W1_D0), px(W1_D1)], "from_floor_px": [0, px(W1_DH)],
                "status": "placed from the photo, not measured; x is from the wall's left end as you face it (the box end)"},
               base_trim("Wall1", g["WALL1"], [(W1_D0 - CAS, W1_D1 + CAS)])]})

walls.append({"wall": 2, "id": "B2", "aliases": ["Entrance band", "Wall 2"], "name": "Entrance band wall plus its bulkhead", "art": True,
  **dims(W, L, "measured"),
  "faces": [
    {"id": "B2", "what": "wall face, floor to the bulkhead underside", "px": [px(W), px(g["BH_UNDER"])], "ratio": round(W / g["BH_UNDER"], 3),
     "from_floor_px": [0, px(g["BH_UNDER"])], "art_file": "art/B2.png", "tex": "tex/B2.jpg"},
    {"id": "B2_bulkhead", "what": f"bulkhead face above the wall face, stands {ftin(g['BH_PROJ'])} proud of the wall", "px": [px(W), px(L - g["BH_UNDER"])],
     "ratio": round(W / (L - g["BH_UNDER"]), 3), "from_floor_px": [px(g["BH_UNDER"]), px(L)], "art_file": "art/B2_bulkhead.png", "tex": "tex/B2_bulkhead.jpg"}],
  "left": {"neighbour": "Wall1", "corner": "inside corner"}, "right": {"neighbour": "B3", "corner": "inside corner"},
  "keepouts": [
    {"what": f"double-door opening, {ftin(g['B2_DOOR_W'])} wide x {ftin(g['B2_DOOR_H'])} high", "x_px": [px(b2s0), px(b2s0 + g["B2_DOOR_W"])],
     "from_floor_px": [0, px(g["B2_DOOR_H"])], "status": "position measured from the B3 corner (14 ft 11 in); the first canvas spec said x 1820 to 2420 and was wrong"},
    {"what": "white casing around the opening, not paintable", "width_px": 40, "status": "4 in, provisional until scaled from the photo"},
    base_trim("B2", W, [(b2s0 - CAS, b2s0 + g["B2_DOOR_W"] + CAS)], "the trim layer is cut to the B2 wall-face canvas (the art/B2.png size), not the bulkhead")],
  "notes": [f"Horizontal split at {px(g['BH_UNDER'])} px from the floor: wall face below, bulkhead face above.",
            "A design may cross onto the bulkhead; deliver the two faces as two files that share the split line."]})

walls.append({"wall": 3, "id": "B3", "aliases": ["Cardio window wall", "Wall 3"], "name": "Cardio window wall band", "art": True,
  **dims(D, H, "length = the direct B2 to M4 reading (60 ft 7 1/2 in); the wall is 12 ft 11 in high for the first 16 ft 10 in from the B2 corner, then 13 ft 7 in"),
  "art_file": "art/B3.png", "tex": "tex/B3.jpg",
  "left": {"neighbour": "B2", "corner": "inside corner"}, "right": {"neighbour": "M4", "corner": "inside corner"},
  "keepouts": [
    {"what": "low-ceiling stretch: the wall stops at the 12 ft 11 in ceiling; the strip above it is not wall", "x_px": [0, px(g["STEP"])], "from_floor_px": [px(L), px(H)]},
    {"what": "Window 1", "x_px": [px(g["lStart"]), px(g["lEnd"])], "from_floor_px": [px(g["SILL"]), px(g["SILL"] + ft(7, 7.5))], "status": "7 ft wide measured; height about 7 ft 7 1/2 in"},
    {"what": "Doors (glass)", "x_px": [px(g["dStart"]), px(g["dEnd"])], "from_floor_px": [0, px(9)]},
    {"what": "Window 2", "x_px": [px(g["rStart"]), px(g["rEnd"])], "from_floor_px": [px(g["SILL"]), px(g["SILL"] + ft(7, 8))], "status": "sill provisional"},
    {"what": "white trim 40 px (4 in) around every opening, not paintable"},
    base_trim("B3", D, [(g["dStart"] - CAS, g["dEnd"] + CAS)], "runs under both windows; breaks only at the glass doors")],
  "notes": ["Openings are placed by working back from the M4 corner."]})

M4W, BAND, XMAX = g["M4W"], g["BAND"], g["XMAX"]; sec = BAND / 3
MIR_H, MIR0, MIR1 = g["MIR_H"], M4W + g["MIR_IN"], XMAX - g["MIR_OUT"]   # mirrors, in Wall 4 feet from the B3 corner
MIR_STATUS = ("PROVISIONAL, not taped. 8 ft tall (Tripp 10-07), standing on the TOP EDGE of the bottom trim, not on the floor. "
              "Start about 8 to 10 ft past the end of M4 and stop about 25 to 30 ft before the M7 corner (Tripp 10-11); "
              f"the model uses the middle of each range, {ftin(g['MIR_IN'])} and {ftin(g['MIR_OUT'])}.")
def clip(a, b, s0, s1):                                   # a range in Wall 4 feet, clipped to a section, in section px
    lo, hi = max(a, s0), min(b, s1)
    return [px(lo - s0), px(hi - s0)] if hi > lo else None
sections = [{"section": 1, "id": "M4", "aliases": ["Wall 4 Section 1"], "what": "the existing painted M4 mural. DO NOT regenerate it.",
             "x_px": [0, px(M4W)], **dims(M4W, H, "49 ft per Tripp Oct 2026"), "art_file": None, "tex": "tex/M4.jpg",
             "layers": {"trim": "layers/trim/M4.png"}}]
for i in range(3):
    s0, s1 = M4W + i * sec, M4W + (i + 1) * sec
    s = {"section": i + 2, "id": f"B4-{i+1}", "aliases": [f"Wall 4 Section {i+2}", f"B4 Mirror Band Section {i+1}"], "x_px": [px(s0), px(s1)],
         **dims(sec, H, "one third of the 146 ft B4 run; the split is a planning convenience, not a feature of the wall"), "art_file": None,
         "mirrors_x_px_in_section": clip(MIR0, MIR1, s0, s1),
         "layers": {"trim": f"layers/trim/B4-{i+1}.png", "mirrors": f"layers/mirrors/B4-{i+1}.png"}}
    sections.append(s)
walls.append({"wall": 4, "id": "M4+B4", "aliases": ["M4", "B4", "B4 Mirror Band", "Mirror Band", "Forward mirror wall", "Wall 4", "the 195 ft wall"],
  "name": "Mirror wall: the M4 mural, then the B4 Mirror Band, the band above the mirrors. One continuous wall, one tape 0 to 195 ft.", "art": True,
  **dims(M4W + BAND, H, "49 ft + 146 ft per Tripp Oct 2026 (V4 said 36 + 159); field sheet 195 ft 0 1/2 in x 13 ft 8 in with an 8 in crown, crown not modelled"),
  "left": {"neighbour": "B3", "corner": "inside corner"}, "right": {"neighbour": "M7", "corner": "inside corner"},
  "sections": sections,
  "section_naming_status": "CONFIRMED by Tripp 2026-10-11: the band right of M4 is B4, called the B4 Mirror Band. B5 is the band on the box face over M6 and is a different wall. Sections B4-1, B4-2, B4-3 stand.",
  "whole_B4": {"id": "B4", "name": "B4 Mirror Band", "x_px": [px(M4W), px(XMAX)], **dims(BAND, H, "146 ft per Tripp Oct 2026, taped 146 ft 0 1/2 in"), "art_file": None, "tex": None},
  "layers": {"trim": "layers/trim/M4-B4.png", "mirrors": "layers/mirrors/M4-B4.png"},
  "keepouts": [
    {"what": "mirrors under the B4 Mirror Band, not paintable. Their own layer over the design.", "x_px": [px(MIR0), px(MIR1)],
     "from_floor_px": [px(BASE), px(BASE + MIR_H)], "length_text": ftin(MIR1 - MIR0), "height_text": ftin(MIR_H),
     "start_range_x_px": [px(M4W + 8), px(M4W + 10)], "stop_range_x_px": [px(XMAX - 30), px(XMAX - 25)],
     "layer": "layers/mirrors/M4-B4.png", "status": MIR_STATUS,
     "band_above": f"From the mirror tops ({ftin(BASE + MIR_H)} up) to the ceiling is about {ftin(H - BASE - MIR_H)}; "
                   f"if the field sheet's 8 in crown is real, the paintable band is about {ftin(H - BASE - MIR_H - ft(0, 8))}."},
    base_trim("M4+B4", XMAX, (), "runs the whole 195 ft; the mirrors stand on it"),
    {"what": f"the M4 / B4 line at {px(M4W)} px (49 ft) and the section lines are flat continuations, not corners"},
    {"what": "the M4 photo on the page is laid on unstretched and runs about 1 ft 6 in past the 49 ft mark onto B4 (foliage and blue wall)"}]})

M7W = g["M7W"]
walls.append({"wall": 5, "id": "M7", "aliases": ["B7", "The Viper", "Separator wall", "Wall 5"], "name": "The Viper", "art": True,
  **dims(M7W, H, "width from V4"), "art_file": "art/M7.png", "tex": "tex/M7.jpg",
  "left": {"neighbour": "B4", "corner": "inside corner"}, "right": {"neighbour": "M8", "corner": "inside corner"},
  "keepouts": [{"what": "door 10 ft x 9 ft, hard against the right end, no trim", "x_px": [px(M7W - 10), px(M7W)], "from_floor_px": [0, px(9)], "status": "per Tripp 2026-10-11"},
               base_trim("M7", M7W, [(M7W - 10, M7W)])]})

M8W = g["M8W"]
walls.append({"wall": 6, "id": "M8", "aliases": ["B6", "The Tiger", "Breakroom wall", "Wall 6"], "name": "The Tiger", "art": True,
  **dims(M8W, H, f"width from V4, close enough per Tripp; the wall plane sits in line with the end of M7, about {ftin(M8Y)} in from the B2 line, provisional"),
  "art_file": "art/M8.png (web copy 8192 x 1547)", "tex": "tex/M8.jpg",
  "left": {"neighbour": "M7", "corner": "inside corner"}, "right": {"neighbour": "East", "corner": "flat continuation, unmeasured"},
  "keepouts": [{"what": "break room and service doors and windows exist; positions come from the photo and are NOT measured; nothing is cut out"},
               base_trim("M8", M8W, (), "runs the full length for now: the M8 door gaps are not cut because the doors are not measured")]})

walls.append({"wall": 7, "id": "East", "name": "Unnamed stretch between the Tiger and the box", "art": False,
  **dims(BOXN - BX, H, "NOT MEASURED, placeholder"), "keepouts": [base_trim("East", BOXN - BX)]})
walls.append({"wall": 8, "id": "BoxEnd", "name": "Box end", "art": False, **dims(g["WALL1"] - M8Y, H, "derived; the box is about 8 ft longer than the females partition"),
  "keepouts": [base_trim("BoxEnd", g["WALL1"] - M8Y)]})
walls.append({"wall": 9, "id": "M6+B5", "aliases": ["M6", "B5", "Box face", "Wall 9"], "name": "Box face, the wings mural and its band. Not the B4 Mirror Band.", "art": False,
  **dims(g["M6W"], H, "width from V4; placed at the Wall 1 end of the box face; its 76 x 86 1/2 in door is not placed; not in the current canvases"),
  "keepouts": [base_trim("M6+B5", g["M6W"], (), "runs the full length for now: the M6 door is not placed, so its trim gap is not cut")]})

spec = {
  "project": "Palmetto Pump House, Phase 2, Zone 3 band and mural walls",
  "generated_from": "index.html measurement constants, PPH Zone 3 Walkthrough V2",
  "version": "2026-10-11 rev 2: bottom trim on every wall, B4 mirrors placed, B4 Mirror Band named",
  "scale": {"px_per_inch": PX, "px_per_foot": 12 * PX, "ppi": 120,
            "note": "10 px = 1 in. Every canvas and keep-out is in these px, measured from the LEFT edge as you face the wall and UP from the floor. Photoshop y from top = canvas height minus y from floor."},
  "eye_level": {"in": inch(g["EYE"]), "px_from_floor": px(g["EYE"]), "text": ftin(g["EYE"])},
  "base_trim": {"height_in": round(inch(BASE), 2), "px": px(BASE), "text": f"{round(inch(BASE))} in", "status": BASE_STATUS,
    "rule": (f"Every wall has a white bottom trim from the floor up to {px(BASE)} px. It is not paintable and it is its own layer, laid over the "
             "wall photo and the design, so a photo that already shows the trim and one that does not end up the same. It breaks at every "
             f"doorway (together with the door casing) and runs under windows. Anything that stands on the trim, like the B4 mirrors, starts at "
             f"its top edge, {px(BASE)} px up, never at the floor.")},
  "layers": {"what": "Transparent PNG overlays at the exact canvas px, one per wall plus one per Wall 4 section. Stack them over a design to check it. Do not paint them into a design.",
    "trim": "layers/trim/<file id>.png, every wall and every Wall 4 section",
    "mirrors": "layers/mirrors/<file id>.png, Wall 4 (M4-B4) and the B4 sections only",
    "file_id": "the wall or section id with + written as - (M4+B4 becomes M4-B4). B2's trim layer is cut to the B2 wall-face canvas.",
    "built_by": "tools/make_layers.py, from this spec. Never hand-edit; rerun it after make_spec.py.",
    "stack_order": "wall photo, then design, then trim and mirrors on top"},
  "orientation": "Left and right are as seen standing in the room facing the wall. The band walks B2 > B3 > M4 > B4 > M7 > M8; the canvases join end to end in that order.",
  "vocabulary": "Every wall has three names that mean the same thing: the wall number (Wall 4), the section (Wall 4 Section 2) and the alias id (B4-1). Accept any; answer with all three. Write 'Section', never the section symbol.",
  "live_site": LIVE, "repo": "https://github.com/TrippArt/PPH-PHASE-2-WALKTHROUGH",
  "file_urls": {"pattern": LIVE + "<path>", "example_photo": LIVE + "tex/B3.jpg", "example_design": LIVE + "art/B3.png", "page_source": LIVE + "index.html"},
  "walls": walls,
  "delivery": {
    "format": "PNG with a transparent background, sRGB",
    "extent": "full image width = the wall or section's full length, left edge = the named left corner or split line; full image height = the full wall height. Never crop to the band alone: where the band sits in the height is part of the design.",
    "size": "either the exact canvas px, or the exact ratio at the largest size the tool allows, with the delivered px stated",
    "naming": "art/<id>.png, for example art/B4-1.png",
    "keepouts": "for the designer's eye only; the 3D model cuts the openings and lays the bottom trim and the mirrors over the design automatically, so a band may run straight across a window or behind a mirror. Keep focal elements out of the doors, the mirrors and the bottom trim.",
    "corners": "a design that turns an inside corner is two files that share the corner edge, column for column",
    "flat_splits": "the M4 / B4 line and the B4 section lines are not corners; neighbouring sections must be continuous across the line"},
  "rules": ["Real scale controls artwork placement. Never deform a wall to fit art.",
            "Do not regenerate the existing M4 mural.",
            "White window and door trim is not paintable.",
            "The bottom trim is not paintable. Mirrors and anything else standing on it start at its top edge, not at the floor.",
            "B4 is the B4 Mirror Band. B5 is the box-face band over M6, a different wall.",
            "Wall 1 stays blank.",
            "M4 and B4 are the same wall.",
            "Do not present provisional values as measured; carry each status string forward.",
            "Do not rename walls or sections; use the names here and raise naming questions with Tripp."],
  "open_questions": ["Bottom trim height (8 in from Tripp's panorama note; not taped).",
                     "Band height and its top and bottom edges above the floor on each wall.",
                     "B2 casing width (sets where the band starts beside the doors).",
                     "Mirror start and stop on B4 (Tripp's estimate: 8 to 10 ft past M4, 25 to 30 ft before the M7 corner; not taped).",
                     "M7 and M8 door details; a wall photo for the B4 run.",
                     "Females partition dimensions; the east stretch; B3 to column 1 distance."]}
out = os.path.join(repo, "pph-zone3-spec.json")
json.dump(spec, open(out, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("wrote", out)
for w in walls:
    print(f"Wall {w['wall']:>2} {w['id']:<8} {w['length_text']:<16} x {w['height_text']:<12} {w['canvas']['px']}  {w['canvas']['ratio_text']}  | {w['status'][:60]}")
print("B2 opening px", walls[1]["keepouts"][0]["x_px"], "| B3 openings", [k.get("x_px") for k in walls[2]["keepouts"][1:4]])
print("W4 sections", [(s["id"], s["x_px"], s["canvas"]["px"], s["canvas"]["ratio_text"], s.get("mirrors_x_px_in_section")) for s in sections])
print("mirrors", walls[3]["keepouts"][0]["x_px"], walls[3]["keepouts"][0]["from_floor_px"], walls[3]["keepouts"][0]["length_text"], "|", walls[3]["keepouts"][0]["band_above"])
print("trim", spec["base_trim"]["px"], "px |", [(w["id"], [k["runs_x_px"] for k in w.get("keepouts", []) if "runs_x_px" in k]) for w in walls])
