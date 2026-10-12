# avatar/

The walker's head. The page draws you as a simple blocky figure in a white PUMP IT! tee (seen in the B4 mirrors while walking, and standing on the floor in Overview and Plan). This folder holds the picture for its head.

- **File:** `avatar/head.png` (that exact name). The current file is Michael's head: face, Palmetto Pump House trucker hat and beard as a transparent cutout, 1224 x 1323 px.
- **A tall cutout like that** (any picture that is not square) is hung on the neck as a thin flat plate, 1.9 ft high, a little in front of the block head, facing the way the figure faces. It is a real object in the room, not a billboard, so the mirror shows it from any angle. Clear pixels are cut away (alpha below half is dropped), so keep the edge clean. The block head stays behind the plate, slimmed to fit inside the cutout, coloured from the picture: its top takes the hat (the top rows), its sides and back take the beard (the bottom rows).
- **A square picture** is painted onto the front of the block head instead: the whole picture becomes the front face, its top rows colour the top of the head and its outer columns the sides and back.
- **Until the file exists** the page draws a placeholder face, so nothing breaks without it.
- **Size:** keep it under about 2 MB; phones load the same file. No `sm/` copy is needed.

Drop the file in, commit, push: no code change needed.
