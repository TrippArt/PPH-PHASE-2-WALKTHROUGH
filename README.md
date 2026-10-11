# PPH Zone 3 Walkthrough V2

Interactive 3D walkthrough of Zone 3 of the Palmetto Pump House gym, Phase 2 mural program, by Tripp Art.

A static site with no build step. `index.html` at the root is the whole app; it loads three.js r128 from cdnjs and the Barlow font from Google Fonts, and every image by relative path.

| Folder | Contents |
|---|---|
| `tex/` | Wall, ceiling and bulkhead textures (JPEG) |
| `art/` | Band and mural artwork as transparent PNGs, web size (long side capped at 8192 px) |
| `sm/` | Phone-size copies (long side 4096 px) of the heavier art and textures |

**Live:** https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/
**Repo:** https://github.com/TrippArt/PPH-PHASE-2-WALKTHROUGH

GitHub Pages serves the `main` branch root; every push to `main` redeploys within about a minute.

## Running it

Serve the repository root with any static file server and open `index.html`. Opening the file directly from disk also works in most browsers because every asset path is relative.

## For ChatGPT and other reviewers

- `GPT_BRIEF.md` is the standing brief: what the project is, how to read a wall back, delivery rules.
- `pph-zone3-spec.json` is the machine-readable wall spec (sizes, canvas px at 10 px = 1 in, ratios, neighbours, keep-outs, status). It is generated from the measurement constants in `index.html` by `tools/make_spec.py`; regenerate it whenever those constants change:

```
python tools/make_spec.py .
```

## Editing

The scene geometry, measurements, wall ids and labels encode surveyed and provisional dimensions. Do not change them as part of a visual edit; dimension changes go through the Phase 2 spec first. Provisional values are not measured values.

The Dropbox copy of this folder under the Phase 2 gig is the editing source. Changes are made there, mirrored into this repository, committed and pushed. The hosted preview rebuilds from the pushed commit.
