## TkinterOpenGL
3D rendering for .obj models in tkinter frame.

### Based on:
- Jonathan Wright's Tkinter - OpenGL Frame using ctypes repo: [jonwright/pyopengltk](https://github.com/jonwright/pyopengltk)
- Andrew's GetIntoGameDev - Youtube tutorial: [OpenGL with Python](https://youtu.be/LCK1qdp_HhQ?list=PLn3eTxaOtL2PDnEVNwOgZFm5xYPr4dUoR)

### Basic usage:
- Put your .obj model in [/OpenGLobj/obj](/OpenGLobj/obj)
- Put your texture image in [/OpenGLobj/textures](/OpenGLobj/textures)
- simple example with the render frame and two dummy buttons:
```python
import tkinter
import TkinterOpenGL as TOGLR


def main():
    root = tkinter.Tk()

    render_frame = TOGLR.TkinterOpenGLrender(root,
                                     "./OpenGLobj/obj/monkey.obj",
                                     "./OpenGLobj/textures/gold.png",
                                     height=600, width=800)
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

### Requirements
- pyopengltk (slightly modified)
- PyOpenGL
- tkinter
- ctypes
- pyrr
- numpy
- pillow



