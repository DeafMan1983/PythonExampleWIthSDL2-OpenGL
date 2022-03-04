import ctypes
import sys
from OpenGL import GL

import sdl2
import numpy

def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"Hello Triangle", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, 800, 600, sdl2.SDL_WINDOW_OPENGL)
    if not window:
        print(sdl2.SDL_GetError())
        return  -1

    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 0)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK, sdl2.SDL_GL_CONTEXT_PROFILE_CORE)
    context = sdl2.SDL_GL_CreateContext(window)
    if not context:
        print(sdl2.SDL_GetError())
        return  -1

    vertex_shader_source = """#version 330 core

        layout(location = 0) in vec2 position;
        layout(location = 1) in vec4 color;

        out vec4 vColor;

        void main()
        {
            vColor = color;
            gl_Position = vec4(position, 0.0, 1.0);
        }"""
    fragment_shader_source = """#version 330 core

        in vec4 vColor;
        out vec4 fragColor;

        void main()
        {
            fragColor = vColor;
        }"""
    vertex_shader = GL.glCreateShader(GL.GL_VERTEX_SHADER)
    GL.glShaderSource(vertex_shader, vertex_shader_source)
    GL.glCompileShader(vertex_shader)

    fragment_shader = GL.glCreateShader(GL.GL_FRAGMENT_SHADER)
    GL.glShaderSource(fragment_shader, fragment_shader_source)
    GL.glCompileShader(fragment_shader)

    shader_program = GL.glCreateProgram()
    GL.glAttachShader(shader_program, vertex_shader)
    GL.glAttachShader(shader_program, fragment_shader)
    GL.glLinkProgram(shader_program)

    GL.glDeleteShader(vertex_shader)
    GL.glDeleteShader(fragment_shader)

    vertices = numpy.array(
        [+0.0, +0.5,
        -0.5, -0.5,
        +0.5, -0.5],
        dtype=numpy.float32
    )
    colors = numpy.array(
        [1, 0, 0, 1,
        0, 1, 0, 1,
        0, 0, 1, 1],
        dtype=numpy.float32
    )

    vao = GL.glGenVertexArrays(1)
    GL.glBindVertexArray(vao)

    vbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices, GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(0, 2, GL.GL_FLOAT, False, 0, None)

    vboCol = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vboCol)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, colors, GL.GL_STATIC_DRAW)
    GL.glVertexAttribPointer(1, 4, GL.GL_FLOAT, False, 0, None)

    GL.glEnableVertexAttribArray(0)
    GL.glEnableVertexAttribArray(1)

    GL.glBindVertexArray(0)

    event = sdl2.SDL_Event()
    running = True
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                running = False

            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False

        GL.glClearColor(1, 0.25, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(shader_program)
        GL.glBindVertexArray(vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)

        sdl2.SDL_GL_SwapWindow(window)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())