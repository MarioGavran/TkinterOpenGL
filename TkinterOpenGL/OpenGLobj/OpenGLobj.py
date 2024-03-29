import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import ctypes
import pyrr
from PIL import Image
import os.path

#########################################################################
#########################################################################
class Cube:

    #########################################################################
    def __init__(self, position, eulers, obj_path, texture_path, cube_id):
        self.cube_id = cube_id
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)
        self.mesh = Mesh(obj_path)
        self.material_texture = Material(texture_path)


#########################################################################
#########################################################################
class Scene:

    #########################################################################
    def __init__(self, *args):
        self.cubes = []
        i = 0
        j = 0
        while i < len(args):
            self.cubes.append(Cube(
                position=[-1+i, 0, -5],
                eulers=[0, 0, 0],
                obj_path=args[i],
                texture_path=args[i+1],
                cube_id=j+1
            ))
            i += 2
            j += 1

        self.lights = Light(
            position=[4, 0, 2],
            color=[1, 1, 1],
            strength=5
        )

    #########################################################################
    def update(self):
        for cube in self.cubes:
            if cube.eulers[2] > 360:
                cube.eulers[2] -= 360


#########################################################################
#########################################################################
class Light:

    #########################################################################
    def __init__(self, position, color, strength):
        self.position = np.array(position, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.strength = strength


#########################################################################
#########################################################################
class OpenGLobj:

    #########################################################################
    def __init__(self, *args, width, height):
        self.clicked = False
        self.mouse_x = None
        self.mouse_y = None
        self.clicked_object_id = None

        # init OpenGL
        glClearColor(1, 1, 1, 1)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=width / height,
            near=0.1, far=10, dtype=np.float32
        )

        shaders_path = os.path.abspath(os.path.dirname(__file__))

        # set all picking Shader variables
        self.pickingShader = self.create_shader(shaders_path + "/shaders/picking_vertex.txt",
                                                shaders_path + "/shaders/picking_fragment.txt")
        glUseProgram(self.pickingShader)
        self.codeVarLocation = glGetUniformLocation(self.pickingShader, "code")
        glBindFragDataLocation(self.pickingShader, 0, "outputF")
        glUniformMatrix4fv(glGetUniformLocation(self.pickingShader, "projection"), 1, GL_FALSE, projection_transform)
        self.pickingModelMatrixLocation = glGetUniformLocation(self.pickingShader, "model")

        # set all regular Shader variables
        self.shader = self.create_shader(shaders_path + "/shaders/vertex.txt",
                                         shaders_path + "/shaders/fragment.txt")
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "image.texture"), 0)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection_transform)
        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        self.lightLocation = {
            "position": glGetUniformLocation(self.shader, "Light.position"),
            "color": glGetUniformLocation(self.shader, "Light.color"),
            "strength": glGetUniformLocation(self.shader, "Light.strength")
        }
        self.cameraPosLoc = glGetUniformLocation(self.shader, "cameraPosition")

        self.scene = Scene(*args)
        self.render()

    #########################################################################
    def create_shader(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragment_filepath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    #########################################################################
    def render(self):
        self.scene.update()

        # refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if self.clicked:
            glUseProgram(self.pickingShader)
        else:
            glUseProgram(self.shader)

            glUniform3fv(self.lightLocation["position"], 1, self.scene.lights.position)
            glUniform3fv(self.lightLocation["color"], 1, self.scene.lights.color)
            glUniform1f(self.lightLocation["strength"], self.scene.lights.strength)
            glUniform3fv(self.cameraPosLoc, 1, [0, 0, 0])

        for i, cube in enumerate(self.scene.cubes):
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(cube.eulers),
                    dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=cube.position,
                    dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)
            if self.clicked:
                glProgramUniform1i(self.pickingShader, self.codeVarLocation, cube.cube_id)
            else:
                cube.material_texture.use()

            glBindVertexArray(cube.mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, cube.mesh.vertex_count)

        if self.clicked:
            self.clicked = False
            data = glReadPixels(self.mouse_x, self.mouse_y, 1, 1, GL_RGBA, GL_UNSIGNED_INT)
            self.clicked_object_id = data[0][0][0] & 255

    #########################################################################
    def quit(self):
        for cube in self.scene.cubes:
            cube.mesh.destroy()
            cube.material_texture.destroy()
        glDeleteProgram(self.shader)
        glDeleteProgram(self.pickingShader)


#########################################################################
#########################################################################
class Mesh:

    #########################################################################
    def __init__(self, filename):
        # xyz
        vertices = self.load_mesh(filename)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # Texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # Normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    #########################################################################
    def load_mesh(self, filename) -> list[float]:
        v = []
        vt = []
        vn = []

        vertices = []

        with open(filename, "r") as file:

            line = file.readline()

            while line:
                words = line.split(" ")
                if words[0] == "v":
                    v.append([float(words[1]),
                              float(words[2]),
                              float(words[3])])
                elif words[0] == "vt":
                    vt.append([float(words[1]),
                               float(words[2])])
                elif words[0] == "vn":
                    vn.append([float(words[1]),
                               float(words[2]),
                               float(words[3])])
                elif words[0] == "f":
                    self.read_faces_data(words, v, vt, vn, vertices)
                line = file.readline()

        return vertices

    #########################################################################
    def read_faces_data(self,
                        words: list[str],
                        v: list[list[float]],
                        vt: list[list[float]],
                        vn: list[list[float]],
                        vertices: list[float]) -> None:
        triangle_count = len(words) - 3

        for i in range(triangle_count):
            self.make_corner(words[1], v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)

    #########################################################################
    def make_corner(self, corner_description: str,
                    v: list[list[float]],
                    vt: list[list[float]],
                    vn: list[list[float]],
                    vertices: list[float]) -> None:
        v_vt_vn = corner_description.split("/")
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)

    #########################################################################
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


#########################################################################
#########################################################################
class Material:

    #########################################################################
    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = Image.open(filepath)
        image_width = image.size[0]
        image_height = image.size[1]
        image_data = image.convert("RGBA").tobytes("raw", "RGBA")
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    #########################################################################
    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    #########################################################################
    def destroy(self):
        glDeleteTextures(1, (self.texture,))

