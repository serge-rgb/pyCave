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
from tga import *
import random

class Sprite:
    '''
    Two dimensional entity displayed as an image.
    Used for explosion-effects and menu graphics
    @params fname: TGA texture filename
    '''
    def __init__(self,scale):
        #Image, position, drawing (tricky)
        self.trans = 0.0
        self.ypos = 0.0
        self.xpos = 0.0
        self.rotate = random.random()*360
        self.scale = random.random()*scale
        self.list = 0
        self.createDisplayList()
        
    def newTexture(self,fname):
        self.image = TgaTexture(fname)
        self.image.newGLTexture()
        
    def setTexture(self,image):
        self.image = image
        
    def draw(self):
        glBindTexture(GL_TEXTURE_2D,self.image.name)
        glPushMatrix()
        glTranslatef(self.xpos,self.ypos,-self.trans) 
        glRotatef(self.rotate,1,0,0)
        glScalef(self.scale,self.scale,self.scale)

        glCallList(self.list)
        glPopMatrix()
        
    def createDisplayList(self):
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        glBegin(GL_QUADS)
        glMultiTexCoord2f(GL_TEXTURE1,1 ,1)
        glVertex3i(0,10,10)
        glMultiTexCoord2f(GL_TEXTURE1,1,0)
        glVertex3i(0,10,-10)
        glMultiTexCoord2f(GL_TEXTURE1,0,0)
        glVertex3i(0,-10,-10)
        glMultiTexCoord2f(GL_TEXTURE1, 0, 1)
        glVertex3i(0,-10,10)
        glEnd()
        glEndList()

if __name__ == '__main__':
    pass

