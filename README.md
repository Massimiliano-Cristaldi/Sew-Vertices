<h1 align=center>Sew Vertices - v0.2</h1>

<div align="center">
  <a href="https://www.youtube.com/watch?v=cc8NwDYefck">
    <img src="https://img.youtube.com/vi/cc8NwDYefck/0.jpg" alt="Sew Vertices - Blender addon demo">
  </a>
</div>

Sew vertices allows you to quickly merge at center all the vertices in a circle selection; to be more specific:
- The operator is added to the right click context menu while in edit mode, and is only available while in vertices select mode
- Running the operator will enable a modal. In this state you can freely zoom in and out, pan and rotate the view, and use CTRL + Z to undo, but other key and mouse functions are suspended; simply press ESC to exit the modal without losing any progress
- While the modal is enabled a sort of circle selection appears near your cursor, indicating which vertices are affected by the operator; use SHIFT + SCROLL WHEEL to grow or shrink the circle
- LEFT CLICKing with the modal enabled causes all the vertices inside the circle to be merged at center; you can hold LEFT CLICK and drag your mouse to affect multiple vertices in succession, and the undo history will only update on mouse release

To install the addon, simply download the .py file in this repository, then open Blender and go to Edit → Preferences → Addons → Install → Open the .py file.
To enable the addon simply check the checkbox.

Sew Vertices was developed and initially tested in Blender 4.1.
Testing is needed in order to ensure compatibility with other versions of Blender.
Further testing is needed to ensure the stability of the addon in Blender 4.1 and other versions.
Feedback in general is greatly appreciated.

Latest update: v0.2
- Swapped SHIFT + MOUSE WHEEL UP and SHIFT + MOUSE WHEEL DOWN events so that selection tool's behavior is consistent with default Blender tools (e.g. proportional editing)
- It is now possible to use numpad keys for orthographic view while modal is running
