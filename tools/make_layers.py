"""Build the overlay layers from pph-zone3-spec.json.
Usage: python make_layers.py <repo-dir>      (run make_spec.py first)

Writes, at the exact canvas px of the spec (10 px = 1 in), transparent PNGs that sit ON TOP of a wall photo and a design:
  layers/trim/<file id>.png     bottom trim, every wall and every Wall 4 section, broken at doorways
  layers/mirrors/<file id>.png  the B4 mirrors, Wall 4 and the B4 sections
and the two small tiles the 3D page repeats along the walls:
  tex/trim.png   4 ft of trim       tex/mirror.png   8 ft x 8 ft of mirror
Every position comes from the spec; nothing here is a measurement of its own."""
import json, os, sys
from PIL import Image, ImageDraw

repo = sys.argv[1]
spec = json.load(open(os.path.join(repo, "pph-zone3-spec.json"), encoding="utf-8"))
TH = spec["base_trim"]["px"]
fid = lambda wid: wid.replace("+", "-")

def column(stops, h):
    """A 1 px wide RGBA column from (row, rgba) stops, linear between them."""
    col = Image.new("RGBA", (1, h))
    for y in range(h):
        for (y0, c0), (y1, c1) in zip(stops, stops[1:]):
            if y0 <= y <= y1:
                t = 0 if y1 == y0 else (y - y0) / (y1 - y0)
                col.putpixel((0, y), tuple(round(a + (b - a) * t) for a, b in zip(c0, c1)))
                break
    return col

# white painted trim: a dark top edge, a soft shadow under the cap, flat white face, a faint floor shadow
TRIM_COL = column([(0, (120, 120, 116, 255)), (1, (120, 120, 116, 255)), (2, (206, 205, 199, 255)), (10, (238, 237, 232, 255)),
                   (TH - 4, (245, 244, 240, 255)), (TH - 1, (214, 213, 207, 255))], TH)
def trim_strip(w): return TRIM_COL.resize((w, TH), Image.NEAREST)

def mirror_panel(w, h, frame=True):
    """Plain glass: a cool vertical gradient with soft diagonal sheen bands, repeating every 960 px (8 ft)."""
    img = column([(0, (198, 212, 218, 255)), (h // 2, (172, 189, 197, 255)), (h - 1, (150, 168, 177, 255))], h).resize((w, h), Image.NEAREST)
    sheen = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(sheen)
    for k in range(-2, w // 960 + 3):
        x = k * 960 + 140
        for off, bw, a in ((0, 150, 46), (210, 40, 34)):
            x0 = x + off
            d.polygon([(x0, 0), (x0 + bw, 0), (x0 + bw - h * 0.6, h), (x0 - h * 0.6, h)], fill=(255, 255, 255, a))
    img = Image.alpha_composite(img, sheen)
    if frame:
        ImageDraw.Draw(img).rectangle([0, 0, w - 1, h - 1], outline=(76, 90, 96, 255), width=6)
    return img

def save(img, rel):
    p = os.path.join(repo, rel); os.makedirs(os.path.dirname(p), exist_ok=True); img.save(p, optimize=True); print("wrote", rel, img.size)

def trim_layer(cw, ch, runs):
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    for x0, x1 in runs:
        if x1 > x0: img.paste(trim_strip(x1 - x0), (x0, ch - TH))
    return img

for w in spec["walls"]:
    cw, ch = w["canvas"]["px"]
    if w["id"] == "B2":                                    # the design canvas is the wall face below the bulkhead
        cw, ch = w["faces"][0]["px"]
    trim = next(k for k in w["keepouts"] if "runs_x_px" in k)
    tl = trim_layer(cw, ch, trim["runs_x_px"])
    save(tl, trim["layer"])
    if w["id"] == "M4+B4":
        mir = next(k for k in w["keepouts"] if k.get("layer", "").startswith("layers/mirrors/"))
        (mx0, mx1), (my0, my1) = mir["x_px"], mir["from_floor_px"]
        ml = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        ml.paste(mirror_panel(mx1 - mx0, my1 - my0), (mx0, ch - my1))
        save(ml, mir["layer"])
        for s in w["sections"]:                            # each section cut from the whole wall, column for column
            sx0, sx1 = s["x_px"]
            save(tl.crop((sx0, 0, sx1, ch)), s["layers"]["trim"])
            if "mirrors" in s["layers"]:
                save(ml.crop((sx0, 0, sx1, ch)), s["layers"]["mirrors"])

# 3D page tiles
save(trim_strip(480), "tex/trim.png")                     # 4 ft
save(mirror_panel(960, 960, frame=False), "tex/mirror.png")  # 8 ft x 8 ft
