This is version 0.1 of my first Blender addon: Sew Vertices

Sew vertices allows you to quickly merge at center all the vertices in a circle selection; to be more specific:
- The operator is added to the right click context menu while in edit mode, and is only available while in vertices select mode
- Running the operator will enable a modal. In this state you can freely zoom in and out, pan and rotate the view, and use CTRL + Z to undo, but other key and mouse functions are suspended; simply press ESC to exit the modal without losing any progress
- While the modal is enabled a sort of circle selection appears near your cursor, indicating which vertices are affected by the operator; use SHIFT + SCROLL WHEEL to grow or shrink the circle
- Left clicking with the modal enabled causes all the vertices inside the circle to be merged at center; you can hold LEFT CLICK and drag your mouse to affect multiple vertices in succession, and the undo history will only update on mouse release

The addon was developed and initially tested in Blender 4.1. 
Testing is needed in order to ensure compatibility with other versions of Blender. 
Further testing is needed to ensure the stability of the addon in Blender 4.1 and other versions.
Feedback in general is greatly appreciated.

Pictures and/or videos coming soon.
