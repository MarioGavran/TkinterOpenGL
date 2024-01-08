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