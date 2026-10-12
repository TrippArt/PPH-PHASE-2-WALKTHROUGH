# GPT brief: PPH Zone 3 band and mural designs

For ChatGPT working in the Palmetto Pump House Phase 2 project. Read this once, then work from the spec file, which is the current truth.

## What this is

Tripp Art is painting a continuous design band plus murals around Zone 3, the lifting hall of the Palmetto Pump House gym. A 3D walkthrough of the hall exists so that everyone, human or model, agrees on which wall is which and how big it is.

- Live walkthrough: https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/
- Repository: https://github.com/TrippArt/PPH-PHASE-2-WALKTHROUGH
- **Spec (fetch this first, every session):** https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/pph-zone3-spec.json
- Page source, if you need the raw constants: https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/index.html
- Any wall photo or current design: `https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/<path>` using the `tex` and `art_file` paths in the spec. Look at them before designing a wall; they are the current state.

The spec is generated from the walkthrough's own measurement constants, so the numbers you fetch are the numbers the 3D model draws. If a pasted number in chat disagrees with the spec, the spec wins, and say so.

## Your job

When Tripp names a wall or a section, you design artwork for it at its true proportions. You do not output geometry and you do not edit the walkthrough. Finished PNGs go back to Tripp, who hands them to Claude Code to place in the Photoshop canvases, export, and republish.

**Before any design, read the wall back.** For the wall or section named, state from the spec:

1. Wall number, section, alias id (all three names).
2. Length and height in feet and inches, and the status string (measured, derived, from V4, provisional).
3. Canvas size in px at 10 px = 1 in, and the ratio.
4. Left and right neighbours and whether each join is an inside corner or a flat continuation.
5. Keep-outs that fall inside it (doors, windows, bulkhead split, the bottom trim, mirrors, above-ceiling strip), with the layer files that show them.

Then wait for Tripp's go. This read-back is the whole point of the spec; it catches a wrong wall before a design is made.

## Scale and orientation

- 10 px = 1 in, 120 px = 1 ft, 120 ppi. Walls are 13 ft 7 in high (1630 px) except B2 and Wall 1 at 12 ft 11 in (1550 px).
- Left and right are as you stand in the room facing the wall. The band walks B2, then B3, then M4 and B4 (one wall), then M7 the Viper, then M8 the Tiger.
- Keep-out boxes are px from the left edge and up from the floor. Eye level is 5 ft 9 in (690 px).

## Bottom trim and mirrors (their own layers)

- **Bottom trim:** every wall has a white bottom trim, 8 in high (80 px), not paintable. It stops at every doorway, together with the door casing, and runs under windows. 8 in is Tripp's working value (his 7 October panorama note). Designs work to true measurements and ratios; an inch either way is fine.
- **B4 mirrors:** Michael bought **48 ft** of mirror (11 October 2026): that is the run. 8 ft tall, standing on the **top edge of the trim**, not on the floor, so 80 to 1040 px up. The model places the run starting 9 ft past M4 (Tripp's working value, 8 to 10 ft): along Wall 4 it spans 6960 to 12720 px (58 ft to 106 ft from the B3 corner), ending 89 ft before the M7 corner. Where along the wall the 48 ft sits is still open, so keep focal elements a foot or so clear of the mirror ends and expect the position to move. In the sections: B4-1 has mirrors from 1080 px to its right edge, B4-2 from its left edge to 960 px, and B4-3 has none.
- Above the mirrors, the B4 Mirror Band has about 4 ft 11 in up to the ceiling (about 4 ft 3 in if the field sheet's 8 in crown is real).
- **Layer files**, transparent PNGs at the exact canvas px: `layers/trim/<id>.png` for every wall and every Wall 4 section; `layers/mirrors/<id>.png` for Wall 4 and B4-1/2/3; `layers/doors/<id>.png`, each door and its casing cut out of the wall photo, for every wall with a door; `layers/sections/<id>.png`, the pink section lines and tags, for Wall 4 and each section. Write `+` as `-` in the file id (`M4-B4`). Fetch them at `https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/layers/...`.
- **Doors:** every door is cut out of the wall in the 3D model and the trim breaks at it. On M8 the three doors and the 5 ft opening at the right end are placed where the photo shows them; the locker-room double doors at the far LEFT end (left edge on the M7 corner, 0 to 800 px, 800 px high) are from Tripp (2026-10-12), not the photo, cut as a standard 6 ft x 6 ft 8 in pair, size provisional. The Tiger's laser beam is meant to hit that door's left trim.
- The stacking order is wall photo, then design, then doors, trim and mirrors, then the pink section guides on top. Lay the layers over your design to check it. Never paint the trim or the mirrors into a design.

## The walls (summary; the spec has the keep-outs)

| Wall | Id | Size | Canvas px | Ratio | Status |
|---|---|---|---|---|---|
| 1 | Wall1 | 19 ft 2 in x 12 ft 11 in | 2300 x 1550 | 1.484 : 1 | measured; stays blank |
| 2 | B2 (+ B2_bulkhead) | 39 ft 1 in x 12 ft 11 in | 4690 x 1550 | 3.026 : 1 | measured; wall face 4690 x 1090 (4.303), bulkhead face 4690 x 460 (10.196) |
| 3 | B3 | 60 ft 7.5 in x 13 ft 7 in | 7275 x 1630 | 4.463 : 1 | length derived; 12 ft 11 in high for the first 16 ft 10 in |
| 4 | M4+B4 | 195 ft x 13 ft 7 in | 23400 x 1630 | 14.356 : 1 | 49 + 146 per Tripp, Oct 2026 |
| 4 Section 1 | M4 | 49 ft x 13 ft 7 in | 5880 x 1630 | 3.607 : 1 | existing mural, never regenerate |
| 4 Sections 2 to 4 | B4-1, B4-2, B4-3 (the B4 Mirror Band) | 49 ft x 13 ft 7 in each, the M4 size | 5880 x 1630 | 3.607 : 1 | Section 4 reaches the M7 corner at 5760 px; its last 120 px are past the corner |
| 5 | M7 | 58 ft 8 in x 13 ft 7 in | 7040 x 1630 | 4.319 : 1 | width from V4 |
| 6 | M8 | 71 ft 11 in x 13 ft 7 in | 8630 x 1630 | 5.294 : 1 | width from V4; doors cut where the photo shows them, plus the locker-room double doors at the far left (Tripp, provisional) |

Walls 7 to 9 (East, BoxEnd, M6+B5) are in the spec for completeness and are not in play for designs yet. **B4 is the B4 Mirror Band. B5 is a different band, on the box face over M6.** Never call the mirror run B5.

## Wall 4 sections

Wall 4 is worked in sections the size of M4, so the M4 mural is never cut: every section is 49 ft x 13 ft 7 in, 5880 x 1630 px. Section 1 is M4 (0 to 5880 px). Section 2 is B4-1 (5880 to 11760), Section 3 is B4-2 (11760 to 17640), Section 4 is B4-3 (17640 to 23520). The wall ends at the M7 corner at 23400, so the last 120 px of Section 4's canvas are past the corner: keep them empty or let the design bleed. In the 3D walkthrough a thin pink dotted line marks each split and a small pink "SECTION n" tag sits at the top right of each section.

## Delivery rules

- PNG, transparent background, sRGB.
- Full image width = the wall or section's full length, left edge = the named left corner or split line. Full image height = the full wall height. Do not crop to the band alone; where the band sits in the height is part of the design.
- Exact canvas px, or the exact ratio at the largest size your tool allows, with the delivered px stated.
- Name files `art/<id>.png`, for example `art/B4-1.png`.
- Keep-outs are for your eye. The model cuts doors and windows and lays the trim and mirrors over the design automatically, so a band may run straight across a window or behind a mirror. Design as if the wall were solid, but do not put a focal element in a door, a mirror or the bottom 80 px.
- A design that turns an inside corner (B2 to B3, B3 to M4, B4 to M7, M7 to M8) is two files that share the corner edge, column for column.
- The M4 / B4 line and the three B4 section lines are flat continuations, not corners. Neighbouring sections must read as one continuous wall across the line.

**If your image tool cannot output the exact ratio:** generate at the widest landscape size available, compose the design inside a centred guide band of the target ratio, and report the crop box in px with the file. Tripp crops to the band. For the long runs it is often better to design one section at a time and carry the edge columns across.

## Rules that do not bend

- Real scale controls artwork placement. Never deform a wall to fit art.
- Do not regenerate the existing M4 mural.
- White window and door trim is not paintable. Wall 1 stays blank.
- The bottom trim is not paintable. Mirrors stand on its top edge, never on the floor.
- M4 and B4 are the same wall.
- Do not present provisional values as measured. Carry the status string forward whenever you quote a number.
- Do not rename walls or sections. Use the spec's names and raise naming questions with Tripp.
- Write "Section", never the section symbol.

## Open questions (do not guess at these)

Band height and its top and bottom edges on each wall; B2 casing width; the M6 door position on the box face; a wall photo for the B4 run.

## Workflow

Tripp names a wall. You read it back from the spec. He says go. You design and deliver the PNG with its px. He hands it to Claude Code, which places it in the Photoshop canvas, exports, republishes the walkthrough, and pushes the commit. You can then review the latest commit or the live page on request.
