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
        "M4W","BAND","XMAX","M7W","M8W","M6W","EYE","rEnd","rStart","dEnd","dStart","lEnd","lStart","SILL","COL_D","COL_FAR"]
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

walls.append({"wall": 1, "id": "Wall1", "aliases": ["B2.5", "Box side wall"], "name": "Box side wall, left of B2. No band, no art.", "art": False,
  **dims(g["WALL1"], L, "measured 19 ft 2 in; the same figure also appears as the column-to-M4 gap, one laser shot of Wall 1 settles it"),
  "tex": "tex/Wall1.jpg",
  "keepouts": [{"what": "doorway", "x_px": [px(W1_D0), px(W1_D1)], "from_floor_px": [0, px(W1_DH)],
                "status": "placed from the photo, not measured; x is from the wall's left end as you face it (the box end)"}]})

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
    {"what": "white casing around the opening, not paintable", "width_px": 40, "status": "4 in, provisional until scaled from the photo"}],
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
    {"what": "white trim 40 px (4 in) around every opening, not paintable"}],
  "notes": ["Openings are placed by working back from the M4 corner."]})

M4W, BAND = g["M4W"], g["BAND"]; sec = BAND / 3
sections = [{"section": 1, "id": "M4", "aliases": ["Wall 4 Section 1"], "what": "the existing painted M4 mural. DO NOT regenerate it.",
             "x_px": [0, px(M4W)], **dims(M4W, H, "49 ft per Tripp Oct 2026"), "art_file": None, "tex": "tex/M4.jpg"}]
for i in range(3):
    sections.append({"section": i + 2, "id": f"B4-{i+1}", "aliases": [f"Wall 4 Section {i+2}"], "x_px": [px(M4W + i * sec), px(M4W + (i + 1) * sec)],
                     **dims(sec, H, "one third of the 146 ft B4 run; the split is a planning convenience, not a feature of the wall"), "art_file": None})
walls.append({"wall": 4, "id": "M4+B4", "aliases": ["M4", "B4", "Forward mirror wall", "Wall 4", "the 195 ft wall"],
  "name": "Mirror wall: the M4 mural, then the B4 band run above the mirrors. One continuous wall, one tape 0 to 195 ft.", "art": True,
  **dims(M4W + BAND, H, "49 ft + 146 ft per Tripp Oct 2026 (V4 said 36 + 159); field sheet 195 ft 0 1/2 in x 13 ft 8 in with an 8 in crown, crown not modelled"),
  "left": {"neighbour": "B3", "corner": "inside corner"}, "right": {"neighbour": "M7", "corner": "inside corner"},
  "sections": sections,
  "section_naming_status": "PROVISIONAL. Tripp has called the run right of M4 'B5'; the walkthrough and V4 call it B4, and B5 is the band on the box face over M6. Section ids B4-1/2/3 wait on Tripp's call. Do not rename.",
  "whole_B4": {"id": "B4", "x_px": [px(M4W), px(M4W + BAND)], **dims(BAND, H, "146 ft per Tripp Oct 2026, taped 146 ft 0 1/2 in"), "art_file": None, "tex": None},
  "keepouts": [
    {"what": "mirrors under the B4 band", "x_px": [px(M4W), px(M4W + BAND)], "from_floor_px": [0, px(8)],
     "status": "NOT in the model. 8 ft tall per Tripp 10-07 (estimate); start about 6 in off the floor and stop 10 to 15 ft before the Viper corner, untaped. The band strip above them is about 5 ft 7 in."},
    {"what": f"the M4 / B4 line at {px(M4W)} px (49 ft) and the section lines are flat continuations, not corners"},
    {"what": "the M4 photo on the page is laid on unstretched and runs about 1 ft 6 in past the 49 ft mark onto B4 (foliage and blue wall)"}]})

M7W = g["M7W"]
walls.append({"wall": 5, "id": "M7", "aliases": ["B7", "The Viper", "Separator wall", "Wall 5"], "name": "The Viper", "art": True,
  **dims(M7W, H, "width from V4"), "art_file": "art/M7.png", "tex": "tex/M7.jpg",
  "left": {"neighbour": "B4", "corner": "inside corner"}, "right": {"neighbour": "M8", "corner": "inside corner"},
  "keepouts": [{"what": "door 10 ft x 9 ft, hard against the right end, no trim", "x_px": [px(M7W - 10), px(M7W)], "from_floor_px": [0, px(9)], "status": "per Tripp 2026-10-11"}]})

M8W = g["M8W"]
walls.append({"wall": 6, "id": "M8", "aliases": ["B6", "The Tiger", "Breakroom wall", "Wall 6"], "name": "The Tiger", "art": True,
  **dims(M8W, H, f"width from V4, close enough per Tripp; the wall plane sits in line with the end of M7, about {ftin(M8Y)} in from the B2 line, provisional"),
  "art_file": "art/M8.png (web copy 8192 x 1547)", "tex": "tex/M8.jpg",
  "left": {"neighbour": "M7", "corner": "inside corner"}, "right": {"neighbour": "East", "corner": "flat continuation, unmeasured"},
  "keepouts": [{"what": "break room and service doors and windows exist; positions come from the photo and are NOT measured; nothing is cut out"}]})

walls.append({"wall": 7, "id": "East", "name": "Unnamed stretch between the Tiger and the box", "art": False,
  **dims(BOXN - BX, H, "NOT MEASURED, placeholder")})
walls.append({"wall": 8, "id": "BoxEnd", "name": "Box end", "art": False, **dims(g["WALL1"] - M8Y, H, "derived; the box is about 8 ft longer than the females partition")})
walls.append({"wall": 9, "id": "M6+B5", "aliases": ["M6", "B5", "Box face", "Wall 9"], "name": "Box face, the wings mural and its band", "art": False,
  **dims(g["M6W"], H, "width from V4; placed at the Wall 1 end of the box face; its 76 x 86 1/2 in door is not placed; not in the current canvases")})

spec = {
  "project": "Palmetto Pump House, Phase 2, Zone 3 band and mural walls",
  "generated_from": "index.html measurement constants, PPH Zone 3 Walkthrough V2",
  "version": "2026-10-11",
  "scale": {"px_per_inch": PX, "px_per_foot": 12 * PX, "ppi": 120,
            "note": "10 px = 1 in. Every canvas and keep-out is in these px, measured from the LEFT edge as you face the wall and UP from the floor. Photoshop y from top = canvas height minus y from floor."},
  "eye_level": {"in": inch(g["EYE"]), "px_from_floor": px(g["EYE"]), "text": ftin(g["EYE"])},
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
    "keepouts": "for the designer's eye only; the 3D model trims openings and trim automatically, so a band may run straight across a window",
    "corners": "a design that turns an inside corner is two files that share the corner edge, column for column",
    "flat_splits": "the M4 / B4 line and the B4 section lines are not corners; neighbouring sections must be continuous across the line"},
  "rules": ["Real scale controls artwork placement. Never deform a wall to fit art.",
            "Do not regenerate the existing M4 mural.",
            "White window and door trim is not paintable.",
            "Wall 1 stays blank.",
            "M4 and B4 are the same wall.",
            "Do not present provisional values as measured; carry each status string forward.",
            "Do not rename walls or sections; use the names here and raise naming questions with Tripp."],
  "open_questions": ["Section ids on Wall 4 (B4-1/2/3 vs Tripp's 'B5').",
                     "Band height and its top and bottom edges above the floor on each wall.",
                     "B2 casing width (sets where the band starts beside the doors).",
                     "Mirror start and stop on B4 (untaped).",
                     "M7 and M8 door details; a wall photo for the B4 run.",
                     "Females partition dimensions; the east stretch; B3 to column 1 distance."]}
out = os.path.join(repo, "pph-zone3-spec.json")
json.dump(spec, open(out, "w", encoding="utf-8", newline="\n"), indent=1, ensure_ascii=False)
print("wrote", out)
for w in walls:
    print(f"Wall {w['wall']:>2} {w['id']:<8} {w['length_text']:<16} x {w['height_text']:<12} {w['canvas']['px']}  {w['canvas']['ratio_text']}  | {w['status'][:60]}")
print("B2 opening px", walls[1]["keepouts"][0]["x_px"], "| B3 openings", [k.get("x_px") for k in walls[2]["keepouts"][1:4]])
print("W4 sections", [(s["id"], s["x_px"], s["canvas"]["px"], s["canvas"]["ratio_text"]) for s in sections])
