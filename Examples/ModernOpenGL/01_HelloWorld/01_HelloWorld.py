import sys
import ctypes
from OpenGL import GL

import sdl2

def run():
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"Hello World", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, 800, 600, sdl2.SDL_WINDOW_OPENGL)
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

        sdl2.SDL_GL_SwapWindow(window)

    sdl2.SDL_GL_DeleteContext(context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())