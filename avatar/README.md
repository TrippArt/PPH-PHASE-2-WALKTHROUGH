# avatar/

The walker's head. The page draws you as a simple blocky figure (seen in the B4 mirrors while walking, and standing on the floor in Overview and Plan). Its head is a cube; this folder holds the picture for the front of that cube.

- **File:** `avatar/head.png` (that exact name).
- **Shape:** square, about 512 x 512 px. The whole picture becomes the front face, so fill the frame with the face.
- **Transparency:** fine. Clear areas show the side colour.
- **Other faces:** the top of the head takes the average colour of the picture's top rows; the sides and back take the average of its left and right edge columns. So hair at the top and skin or hair at the edges give the cube the right colours on their own.
- **Until the file exists** the page draws a placeholder face, so nothing breaks without it.

Drop the file in, commit, push: no code change needed.
