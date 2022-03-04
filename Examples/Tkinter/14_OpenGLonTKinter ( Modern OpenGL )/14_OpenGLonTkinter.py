import time
import tkinter
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
from pyopengltk import OpenGLFrame

class AppOgl(OpenGLFrame):

    def initgl(self):
        """Initalize gl states when the frame is created"""
        glViewport(0, 0, self.width, self.height)
        glClearColor(1.0, 0.25, 0.0, 1.0)

    def redraw(self):
        """Render a single frame"""
        glClear(GL_COLOR_BUFFER_BIT)
        # Start vertex and fragment sahders
        VERTEX_SHADER = """#version 330
            in vec4 position;
            void main()
            {
                gl_Position = position;
            }"""
        
        
        
        FRAGMENT_SHADER = """#version 330
        
            void main()
            {
                gl_FragColor = vec4(1.0f, 1.0f, 1.0f,1.0f);
            }"""

        # What is fuck with compileShader and compileProgram - It looks cheating!!!
        # Please use original Modern OpenGL why not use hlCreateShader, glShaderSource and 
        # glCreateProgram, glAttachShader, glCompileSHader and glLinkProgram  
        vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
        shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    
        triangles = [-0.5, -0.5, 0.0,
                    0.5, -0.5, 0.0,
                    0.0, 0.5, 0.0]
    
        triangles = np.array(triangles, dtype=np.float32)
    
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, triangles.nbytes, triangles, GL_STATIC_DRAW)
    
        position = glGetAttribLocation(shaderProgram, 'position')
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(position)

        glUseProgram(shaderProgram)
  
        glDrawArrays(GL_TRIANGLES, 0, 3)
    
        glUseProgram(0)

if __name__ == '__main__':
    root = tkinter.Tk()
    root.title("Modern OpenGL on Tkinter")
    app = AppOgl(root, width=480, height=320)
    app.pack(fill=tkinter.BOTH, expand=tkinter.YES)
    app.animate = 1
    app.after(100, app.printContext)
    app.mainloop()