## TkinterOpenGL
3D rendering for .obj models in tkinter frame.

### Based on:
- Jonathan Wright's Tkinter - OpenGL Frame using ctypes repo: [jonwright/pyopengltk](https://github.com/jonwright/pyopengltk)
- Andrew's GetIntoGameDev - Youtube tutorial: [OpenGL with Python](https://youtu.be/LCK1qdp_HhQ?list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR)

### Thanks to:
- Andrew from GetIntoGameDev and Khronos forum for help and support

### Basic usage:
- Place your .obj model in [/OpenGLobj/obj](/OpenGLobj/obj)
- Place your texture image in [/OpenGLobj/textures](/OpenGLobj/textures)
- Here is a simple example with the render frame and two dummy buttons below.

### Note the "TkinterOpenGL()" call: 
- The 'root' argument is positional-only, and must come first in the list. 
- The .obj and texture paths are variable length arguments and must come in pairs of .obj and texture files. 
- The 'width' and 'height' are keyword-only arguments, and they must be defined.

```python
import tkinter
from TkinterOpenGL import TkinterOpenGL


def main():
    root = tkinter.Tk()

    render_frame = TkinterOpenGL(root,
                                 "./OpenGLobj/obj/monkey.obj",
                                 "./OpenGLobj/textures/gold.png",
                                 "./OpenGLobj/obj/monkey.obj",
                                 "./OpenGLobj/textures/gold.png",
                                 height=480, width=640)
    render_frame.animate = 10
    render_frame.grid(row=0, column=0)

    button1 = tkinter.Button(root, text="btn1")
    button1.grid(row=1, column=0, sticky="ns")
    button2 = tkinter.Button(root, text="btn2")
    button2.grid(row=2, column=0, sticky="ns")

    return render_frame.mainloop()


if __name__ == "__main__":
    main()
```
- demo:
<img src="images/demo.gif">

### Controls:
- Left-click on object to move it in X-Y directions.
- Left-click on empty space to move all objects. (Pan)
- Right click on object to rotate it.
- Scroll up and down while over an object to move it in Z direction 
- Scroll up and down while over empty space to move all objects in Z direction (Zoom)
- Click scroll on object to rotate it around Z-axis

### Requirements
- pyopengltk
- PyOpenGL
- tkinter
- ctypes
- pyrr
- numpy
- pillow



