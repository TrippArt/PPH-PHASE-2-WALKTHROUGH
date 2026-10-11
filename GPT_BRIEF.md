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
5. Keep-outs that fall inside it (doors, windows, bulkhead split, mirrors, above-ceiling strip).

Then wait for Tripp's go. This read-back is the whole point of the spec; it catches a wrong wall before a design is made.

## Scale and orientation

- 10 px = 1 in, 120 px = 1 ft, 120 ppi. Walls are 13 ft 7 in high (1630 px) except B2 and Wall 1 at 12 ft 11 in (1550 px).
- Left and right are as you stand in the room facing the wall. The band walks B2, then B3, then M4 and B4 (one wall), then M7 the Viper, then M8 the Tiger.
- Keep-out boxes are px from the left edge and up from the floor. Eye level is 5 ft 9 in (690 px).

## The walls (summary; the spec has the keep-outs)

| Wall | Id | Size | Canvas px | Ratio | Status |
|---|---|---|---|---|---|
| 1 | Wall1 | 19 ft 2 in x 12 ft 11 in | 2300 x 1550 | 1.484 : 1 | measured; stays blank |
| 2 | B2 (+ B2_bulkhead) | 39 ft 1 in x 12 ft 11 in | 4690 x 1550 | 3.026 : 1 | measured; wall face 4690 x 1090 (4.303), bulkhead face 4690 x 460 (10.196) |
| 3 | B3 | 60 ft 7.5 in x 13 ft 7 in | 7275 x 1630 | 4.463 : 1 | length derived; 12 ft 11 in high for the first 16 ft 10 in |
| 4 | M4+B4 | 195 ft x 13 ft 7 in | 23400 x 1630 | 14.356 : 1 | 49 + 146 per Tripp, Oct 2026 |
| 4 Section 1 | M4 | 49 ft x 13 ft 7 in | 5880 x 1630 | 3.607 : 1 | existing mural, never regenerate |
| 4 Sections 2 to 4 | B4-1, B4-2, B4-3 | 48 ft 8 in x 13 ft 7 in each | 5840 x 1630 | 3.583 : 1 | section ids provisional |
| 5 | M7 | 58 ft 8 in x 13 ft 7 in | 7040 x 1630 | 4.319 : 1 | width from V4 |
| 6 | M8 | 71 ft 11 in x 13 ft 7 in | 8630 x 1630 | 5.294 : 1 | width from V4 |

Walls 7 to 9 (East, BoxEnd, M6+B5) are in the spec for completeness and are not in play for designs yet.

## Delivery rules

- PNG, transparent background, sRGB.
- Full image width = the wall or section's full length, left edge = the named left corner or split line. Full image height = the full wall height. Do not crop to the band alone; where the band sits in the height is part of the design.
- Exact canvas px, or the exact ratio at the largest size your tool allows, with the delivered px stated.
- Name files `art/<id>.png`, for example `art/B4-1.png`.
- Keep-outs are for your eye. The model trims doors, windows and trim automatically, so a band may run straight across a window. Design as if the wall were solid, but do not put a focal element where a door is.
- A design that turns an inside corner (B2 to B3, B3 to M4, B4 to M7, M7 to M8) is two files that share the corner edge, column for column.
- The M4 / B4 line and the three B4 section lines are flat continuations, not corners. Neighbouring sections must read as one continuous wall across the line.

**If your image tool cannot output the exact ratio:** generate at the widest landscape size available, compose the design inside a centred guide band of the target ratio, and report the crop box in px with the file. Tripp crops to the band. For the long runs it is often better to design one section at a time and carry the edge columns across.

## Rules that do not bend

- Real scale controls artwork placement. Never deform a wall to fit art.
- Do not regenerate the existing M4 mural.
- White window and door trim is not paintable. Wall 1 stays blank.
- M4 and B4 are the same wall.
- Do not present provisional values as measured. Carry the status string forward whenever you quote a number.
- Do not rename walls or sections. Use the spec's names and raise naming questions with Tripp.
- Write "Section", never the section symbol.

## Open questions (do not guess at these)

Section ids on Wall 4 (B4-1/2/3 vs Tripp's "B5"); band height and its top and bottom edges on each wall; B2 casing width; mirror start and stop on B4; M7 and M8 door details; a wall photo for the B4 run.

## Workflow

Tripp names a wall. You read it back from the spec. He says go. You design and deliver the PNG with its px. He hands it to Claude Code, which places it in the Photoshop canvas, exports, republishes the walkthrough, and pushes the commit. You can then review the latest commit or the live page on request.
