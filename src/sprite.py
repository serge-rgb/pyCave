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

#from OpenGL.GL import *
import interface as intf
from tga import *
import random

class Sprite:
    '''
    Two dimensional entity displayed as an image.
    Used for explosion-effects and menu graphics
    @params fname: TGA texture filename
    '''
    def __init__(self,scale=1,randomize=False):
        #Image, position, drawing (tricky)
        self.trans = 0.0
        self.ypos = 0.0
        self.xpos = 0.0
        
        if randomize:
            self.rotate = random.random()*360
            self.scale = random.random()*scale
        else:
            self.rotate = 0
            self.scale = scale
            
        self.list = 0

        self._createDisplayList()
        
    def newTexture(self,fname):
        self.image = TgaTexture(fname)
        self.image.newGLTexture()
        
    def setTexture(self,image):
        self.image = image
        
    def draw(self):
        intf.glBindTexture(intf.GL_TEXTURE_2D,self.image.name)
        intf.glPushMatrix()
        intf.glTranslatef(self.xpos,self.ypos,-self.trans) 
        intf.glRotatef(self.rotate,1,0,0)
        intf.glScalef(self.scale,self.scale,self.scale)

        intf.glCallList(self.list)
        intf.glPopMatrix()
        
    def _createDisplayList(self):
        self.list = intf.glGenLists(1)
        intf.glNewList(self.list,intf.GL_COMPILE)
        intf.glBegin(intf.GL_QUADS)
        intf.glMultiTexCoord2f(intf.GL_TEXTURE1,1 ,1)
        intf.glVertex3i(0,10,10)
        intf.glMultiTexCoord2f(intf.GL_TEXTURE1,1,0)
        intf.glVertex3i(0,10,-10)
        intf.glMultiTexCoord2f(intf.GL_TEXTURE1,0,0)
        intf.glVertex3i(0,-10,-10)
        intf.glMultiTexCoord2f(intf.GL_TEXTURE1, 0, 1)
        intf.glVertex3i(0,-10,10)
        intf.glEnd()
        intf.glEndList()

if __name__ == '__main__':
    pass

