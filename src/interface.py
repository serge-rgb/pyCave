#    This file is part of pyCave.
#
#    pyCave is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyCave is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyCave.  If not, see <http://www.gnu.org/licenses/>.


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import cProfile

class Window:
    def __init__(self): 
        self.w = 800
        self.h = 500
        self.aspect = float(self.w) / float(self.h)
        self.pos = (350,100)
        self.title = "Cave Game"
    
    def recalcAspect(self):
        self.aspect = float(self.w) / float(self.h)
        
class Interface:
    '''
    Interface to GLUT for window management.
    '''
    def __init__(self):
        self.win = Window()
        glutInit([])
        glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL )
        glutInitWindowSize (self.win.w,self.win.h)
        glutInitWindowPosition (self.win.pos[0],self.win.pos[1])
        glClearStencil(0x1) 
        glutCreateWindow(self.win.title)
        
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc(self.keyboardUp)
        glutIgnoreKeyRepeat(1)
        glutIdleFunc(self.idle)
       # glutPassiveMotionFunc(self.passiveMotion)
    def display(self):
        pass
    
    def reshape(self,w,h):
        self.win.w = w
        self.win.h = h
        self.win.recalcAspect()
        glViewport(0,0,w,h)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def keyboard(self,key,x,y):
        if key == 'q':
            self.clean()
        
    def keyboardUp(self,key,x,y):
        pass
    
    def idle(self):
        pass
    
    def passiveMotion(self,x,y):
        pass
    
    def mainLoop(self):
        glutMainLoop()

    def clean(self):
        sys.exit()
