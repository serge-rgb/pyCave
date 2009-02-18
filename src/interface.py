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
import music
import time
import glutils

class Window:
    def __init__(self,title): 
        self.w = 1024
        self.h = 540
        self.aspect = float(self.w) / float(self.h)
        self.pos = (350,100)
        self.title = title
        self.identifier = -1
    
    def recalcAspect(self):
        self.aspect = float(self.w) / float(self.h)

win = Window("pyCave")
        
def initGraphics():
    glutInit([])
    glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
    glutInitWindowSize (win.w,win.h)
    glutInitWindowPosition (win.pos[0],win.pos[1])
    glClearStencil(0x1) 
    glutCreateWindow(win.title)
    
class Interface:
    '''
    Interface to GLUT for window management.
    '''
    def __init__(self):
#        self.win = Window()
        self.win = win        
        glutIgnoreKeyRepeat(1)
        self.getGlutControl()
    
    def getGlutControl(self):
        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)
        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc(self.keyboardUp)
        glutIdleFunc(self.idle)
        
    def display(self):
        '''
        This will be inherited and used by the game and renderer.
        '''
        pass
    
    def reshape(self,w,h):
        win.w = w
        win.h = h
        win.recalcAspect()
        glViewport(0,0,w,h)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
    def keyboard(self,key,x,y):
        key = key.lower()
        if key == 'q' or ord(key)==0x1b: #0x1b == exit
            self.clean()
        if key == 'm':
           music.mute()
            
        
    def keyboardUp(self,key,x,y):
        pass
    
    def idle(self):
        pass
    
    def passiveMotion(self,x,y):
        pass
    
    def mainLoop(self):
        glutMainLoop()

    def clean(self):
        pass
        #glutLeaveMainLoop()
        #import main
        #main.reboot()
        
if __name__ == '__main__':
    from main import *
