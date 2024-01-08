import tkinter
from pyopengltk import OpenGLFrame
from OpenGL import GL
from OpenGL import GLU
from OpenGLobj import OpenGLobj as oGLobj


class CubeSpinner(OpenGLFrame):
    def __init__(self, master, filepath, width, height):
        super().__init__(master=master, width=width, height=height)

        self.filepath = filepath

        self.oglobj = None

        # Mouse movement instance variables
        self.B1x1 = None
        self.B1y1 = None
        self.B2x1 = None
        self.B2y1 = None
        self.B3y1 = None
        self.B3x1 = None

    def initgl(self):
        GL.glLoadIdentity()
        GLU.gluPerspective(45, (self.width / self.height), 0.1, 50.0)
        GL.glTranslatef(0.0, 0.0, -5)

        # Mouse
        self.bind('<Button-1>', self.MouseB1Click)
        self.bind('<B1-Motion>', self.MouseB1Move)

        self.bind('<Button-2>', self.MouseB2Click)
        self.bind('<B2-Motion>', self.MouseB2Move)

        self.bind('<Button-3>', self.MouseB3Click)
        self.bind('<B3-Motion>', self.MouseB3Move)

        self.bind('<Button-4>', self.MouseB4)
        self.bind('<Button-5>', self.MouseB5)

        self.oglobj = oGLobj.OpenGLobj(self.filepath)

    def redraw(self):
        pass
        #GL.glRotatef(1, 3, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.oglobj.mainloop()
        #Cube()

    ##############################################################
    def MouseB1Click(self, event):
        self.B1x1 = event.x
        self.B1y1 = event.y

    ##############################################################
    def MouseB1Move(self, event):
        self.oglobj.cube.position[0] += (event.x - self.B1x1) / 300
        self.oglobj.cube.position[1] -= (event.y - self.B1y1) / 300

        self.B1x1 = event.x
        self.B1y1 = event.y

    ##############################################################
    def MouseB2Click(self, event):
        self.B2x1 = event.x
        self.B2y1 = event.y

    ##############################################################
    def MouseB2Move(self, event):
        # self._angle_y += -(event.x - self.B3x1) / 50
        self.oglobj.cube.eulers[1] += -(event.x - self.B2x1) / 10
        # self._angle_x += (event.y - self.B3y1) / 50
        self.oglobj.cube.eulers[1] -= (event.y - self.B2y1) / 10

        self.B2x1 = event.x
        self.B2y1 = event.y

    ##############################################################
    def MouseB3Click(self, event):
        self.B3x1 = event.x
        self.B3y1 = event.y

    ##############################################################
    def MouseB3Move(self, event):
        # self._angle_y += -(event.x - self.B3x1) / 50
        self.oglobj.cube.eulers[2] += -(event.x - self.B3x1) / 10
        # self._angle_x += (event.y - self.B3y1) / 50
        self.oglobj.cube.eulers[0] -= (event.y - self.B3y1) / 10

        self.B3x1 = event.x
        self.B3y1 = event.y

    ##############################################################
    def MouseB4(self, event):
        self.oglobj.cube.position[2] += 1 / 10

    ###############################################################
    def MouseB5(self, event):
        self.oglobj.cube.position[2] -= 1 / 10


def main():
    root = tkinter.Tk()

    frm1 = CubeSpinner(root, "./OpenGLobj/obj/monkey.obj",  height=600, width=800)
    frm1.animate = 10
    frm1.grid(row=0, column=0)

    frm2 = CubeSpinner(root, "./OpenGLobj/obj/MaleLow.obj", height=600, width=800)
    frm2.animate = 10
    frm2.grid(row=0, column=1)

    button = tkinter.Button(root, text="btn1")
    button.grid(row=1, column=0, sticky="ns")

    return frm1.mainloop(), frm2.mainloop()


if __name__ == "__main__":
    main()
