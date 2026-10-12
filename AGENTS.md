# AGENTS.md: rules for AI agents working in this repo

You are working on the **PPH Zone 3 Walkthrough V2**, a walkable 3D model of Zone 3 of the Palmetto Pump House gym, used by Tripp Art LLC to plan murals and a painted band. People and AI models use it to agree on which wall is which and exactly how big it is. **Tripp owns this repo and approves every merge.** Read this file before you change anything.

Live site: https://trippart.github.io/PPH-PHASE-2-WALKTHROUGH/ (GitHub Pages serves `main` and redeploys about a minute after a merge).

## What is where

| Path | What it is | Edit it? |
|---|---|---|
| `index.html` | The whole app: three.js r128 from cdnjs, no build step. Holds the measurement constants. | Yes, carefully (rules below) |
| `pph-zone3-spec.json` | Machine-readable wall spec, GENERATED from `index.html` | Never by hand |
| `layers/` | Overlay PNGs (trim, mirrors, doors, pink section guides), GENERATED from the spec | Never by hand |
| `tex/trim.png`, `tex/mirror.png` | Tiles the page repeats, GENERATED | Never by hand |
| `tex/` (other files) | Wall photos and the ceiling tile (JPEG) | Only when asked |
| `art/` | Tripp's designs, transparent PNGs, long side at most 8192 px | Only when asked |
| `avatar/head.png` | The walker's head (Michael): a transparent cutout PNG hung on the neck as a thin plate, see `avatar/README.md`. A square PNG is painted onto the block head instead; a placeholder face is drawn until the file exists | Only when asked |
| `sm/` | Phone copies of the heavy images, long side 4096 px | Keep in step with `art/` and `tex/` |
| `tools/make_spec.py`, `tools/make_layers.py` | Generators (Python 3 + Pillow) | Yes, if the task is about them |
| `markups.json` | The team's wall markups, written by the markup bot from "[markup]" issues (`.github/workflows/markups.yml` + `tools/add_markup.py`). Capped at 200 KB; past that it resets | Only to delete marks, and only when asked |
| `GPT_BRIEF.md` | Standing brief for ChatGPT design work | Keep in step with the spec |

## Rules that do not bend

1. **`index.html` is the dimension authority.** Every length lives in the block that starts `/* ---------- measurements (decimal feet) ---------- */`. Do not change a number there unless the person you are working for says it came from Tripp, and name the old and new values in your pull request.
2. **Never hand-edit generated files.** After any change to the measurement block, a door, the trim, the mirrors or the sections, run both generators and commit what they produce:
   ```
   python tools/make_spec.py .
   python tools/make_layers.py .
   ```
3. **Names are fixed.** Walls: `Wall1`, `B2` (+ `B2_bulkhead`), `B3`, `M4+B4`, `M7` (the Viper), `M8` (the Tiger), `East`, `BoxEnd`, `M6+B5`. **B4 is the "B4 Mirror Band"**, the band above the mirrors to the right of M4. **B5 is a different band**, on the box face over M6. Wall 4 sections: Section 1 = `M4`, Sections 2 to 4 = `B4-1`, `B4-2`, `B4-3`, each the M4 size (49 ft x 13 ft 7 in). Do not rename anything; raise naming questions with Tripp. Write "Section", never the section symbol.
4. **Never regenerate or alter the M4 mural.** Wall 1 stays blank.
5. **Keep the status of every number honest.** Label colours: white = measured, yellow = worked out from other measurements or Tripp's working value, orange = provisional. Do not present a provisional value as measured.
6. **Stay small.** No frameworks, no bundler, no new dependencies, no new pages. Keep the single `index.html`. It must keep working on phones (touch controls, 4096 px textures from `sm/`).
7. **Layers stack in this order:** wall photo, then design, then doors, bottom trim and mirrors, then the pink section guides, the eye line and the tape on top. Mirrors stand on the top edge of the 8 in bottom trim, never on the floor. The trim breaks at every door, together with the door casing.
8. **Workflow:** make a branch, keep the change focused, open a pull request into `main` and fill in the template. Never push to `main`, never force-push, never change repo settings, GitHub Pages settings or `.github/` workflows.
9. **Do not commit** secrets, raw camera files, files over about 10 MB, or anything that is not part of the site.

## Finding your way around `index.html`

Search for these names: the measurement block (constants) · `buildWall` (walls, openings, casing) · `baseTrim` (bottom trim) · `MIR_S0` (mirrors) · `buildLabels` (wall names, notes, corners) · `buildSections` (pink section lines and tags) · `SPOTS` (the "Stand at" menu) · `applyToggles` (menu checkboxes) · `renderMirror` (the live reflection in the B4 mirrors) · `avatar`, `updateAvatar` and `avatarView` (the blocky figure, its three-position walk, first-person arms) · `markTick`, `showStroke` and `markSave` (right-mouse wall markups and the save-to-issue flow) · `PHOTOS` and `ART` (which image goes on which wall) · `RUNS` (the tape measure).

Designs attach to a whole wall skin (`ART` map). B4 carries `art/B4.png`, the three-section Mirror Band composite as one image across the 146 ft wall (a rough, trimmed to length with the Viper scales pinned at the M7 corner). The B4 sections do not have their own skins yet. If a task needs per-section artwork on B4, propose the approach in the pull request before building it.

## Test before you open the pull request

```
python -m http.server 8000
```
Open http://localhost:8000, check the browser console for errors, use the menu's "Stand at" buttons to walk to the wall you changed, and try a phone-sized window. Say in the pull request what you checked.
