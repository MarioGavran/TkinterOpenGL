from pyopengltk import OpenGLFrame
from .OpenGLobj import OpenGLobj


class TkinterOpenGL(OpenGLFrame):
    def __init__(self, master, /, *args, width, height):
        super().__init__(master=master, width=width, height=height)

        self.paths = args

        self.oglobj = None

        # Mouse movement instance variables
        self.B1x1 = None
        self.B1y1 = None
        self.B2x1 = None
        self.B2y1 = None
        self.B3y1 = None
        self.B3x1 = None

    def initgl(self):
        # Mouse
        self.bind('<Button-1>', self.MouseB1Click)
        self.bind('<B1-Motion>', self.MouseB1Move)

        self.bind('<Button-2>', self.MouseB2Click)
        self.bind('<B2-Motion>', self.MouseB2Move)

        self.bind('<Button-3>', self.MouseB3Click)
        self.bind('<B3-Motion>', self.MouseB3Move)

        self.bind('<Button-4>', self.MouseB4)
        self.bind('<Button-5>', self.MouseB5)

        self.oglobj = OpenGLobj.OpenGLobj(*self.paths, width=self.width, height=self.height)

    def redraw(self):
        self.oglobj.render()

    ##############################################################
    def MouseB1Click(self, event):
        self.oglobj.clicked = True

        self.B1x1 = event.x
        self.B1y1 = event.y

        self.oglobj.mouse_x = event.x
        self.oglobj.mouse_y = self.height - event.y

        self.oglobj.render()

    ##############################################################
    def MouseB1Move(self, event):
        if self.oglobj.clicked_object_id is None or self.oglobj.clicked_object_id > len(self.oglobj.scene.cubes):
            for cube in self.oglobj.scene.cubes:
                cube.position[0] += (event.x - self.B1x1) / 300
                cube.position[1] -= (event.y - self.B1y1) / 300
            self.B1x1 = event.x
            self.B1y1 = event.y
            return

        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].position[0] += (event.x - self.B1x1) / 300
        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].position[1] -= (event.y - self.B1y1) / 300

        self.B1x1 = event.x
        self.B1y1 = event.y

    ##############################################################
    def MouseB2Click(self, event):
        self.oglobj.clicked = True

        self.B2x1 = event.x
        self.B2y1 = event.y

        self.oglobj.mouse_x = event.x
        self.oglobj.mouse_y = self.height - event.y

        self.oglobj.render()

    ##############################################################
    def MouseB2Move(self, event):
        if self.oglobj.clicked_object_id > len(self.oglobj.scene.cubes):
            return

        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].eulers[1] += -(event.x - self.B2x1) / 10
        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].eulers[1] -= (event.y - self.B2y1) / 10

        self.B2x1 = event.x
        self.B2y1 = event.y

    ##############################################################
    def MouseB3Click(self, event):
        self.oglobj.clicked = True

        self.B3x1 = event.x
        self.B3y1 = event.y

        self.oglobj.mouse_x = event.x
        self.oglobj.mouse_y = self.height - event.y

        self.oglobj.render()

    ##############################################################
    def MouseB3Move(self, event):
        if self.oglobj.clicked_object_id > len(self.oglobj.scene.cubes):
            return

        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].eulers[2] += -(event.x - self.B3x1) / 10
        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].eulers[0] -= (event.y - self.B3y1) / 10

        self.B3x1 = event.x
        self.B3y1 = event.y

    ##############################################################
    def MouseB4(self, event):
        self.oglobj.clicked = True
        self.oglobj.mouse_x = event.x
        self.oglobj.mouse_y = self.height - event.y

        self.oglobj.render()

        if self.oglobj.clicked_object_id is None or self.oglobj.clicked_object_id > len(self.oglobj.scene.cubes):
            for cube in self.oglobj.scene.cubes:
                cube.position[2] += 1 / 10
            return

        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].position[2] += 1 / 10

    ###############################################################
    def MouseB5(self, event):
        self.oglobj.clicked = True
        self.oglobj.mouse_x = event.x
        self.oglobj.mouse_y = self.height - event.y

        self.oglobj.render()

        if self.oglobj.clicked_object_id is None or self.oglobj.clicked_object_id > len(self.oglobj.scene.cubes):
            for cube in self.oglobj.scene.cubes:
                cube.position[2] -= 1 / 10
            return

        self.oglobj.scene.cubes[self.oglobj.clicked_object_id - 1].position[2] -= 1 / 10
