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
from OpenGL.GL.ARB.depth_texture import *
from OpenGL.GL.ARB.shadow_ambient import *
from OpenGL.GL.EXT.framebuffer_object import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
#import c_module


class Light:
    '''
    example: light(engine,(1,1,1,1) ,(10,0,1) ,GL_LIGHT0, True)
    '''
    def __init__(self, engine, color, pos, num, casts_shadows):
        self.pos = pos
        self.look = (0,0,0)
        
        self.color = color
        self.num = num
        self.casts_shadows = casts_shadows
        
        glLightfv(self.num, GL_POSITION, pos)
        glLightfv(self.num, GL_DIFFUSE, color)
        glLightfv(self.num, GL_SPECULAR, color)
#        glLightf (self.num, GL_SPOT_CUTOFF, 40.0)
        
        if self.casts_shadows:
            self.shadowMap = ShadowMap(engine,self)
    
    def move(self, sum):
        self.pos = (self.pos[0] + sum[0] , self.pos[1]+sum[1], self.pos[2] + sum[2])
        self.look =(self.look[0] + sum[0] , self.look[1]+sum[1], self.look[2] + sum[2]) 
        glLightfv(self.num, GL_POSITION, self.pos)
    
    def on(self):
        glEnable(self.num)
    
    def off(self):
        glDisable(self.num)

near = 50
far = 350
class ShadowMap:
    def __init__(self,engine,light):
        self.fov = 60
        self.engine = engine
        self.size = 512
        self.name = glGenTextures(1)
        self.dtexture = glGenTextures(1)
        self.light = light
        self.disabled = False
        self.fbo = 0

        hasDepthTex = glInitDepthTextureARB()
        hasFbo = glInitFramebufferObjectEXT()
        hasAmbient = glInitShadowAmbientARB()

        if not hasFbo or not hasDepthTex:
            print 'No framebuffer object Extension!!!'
            self.disabled = True
            return

        glBindTexture(GL_TEXTURE_2D,self.dtexture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT , self.size, self.size, 0,GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, None)

        texfilter = GL_LINEAR
#        texfilter = GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, texfilter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, texfilter)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FUNC,GL_LEQUAL)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_MODE,GL_COMPARE_R_TO_TEXTURE)

        self.fbo = glGenFramebuffersEXT(1)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.fbo)
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,GL_DEPTH_ATTACHMENT_EXT,#GL_COLOR_ATTACHMENT0_EXT,
                                  GL_TEXTURE_2D,self.dtexture,0)
        glDrawBuffer(GL_NONE);          

        enum = glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)

        if enum == GL_FRAMEBUFFER_COMPLETE_EXT:
            pass
        if enum == GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT:
            print 'Dimension error'
        if enum == GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT:
            print 'Attachment error'
        if enum == GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT:
            print 'draw error'
        
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
          
        print 'SHADOW MAP: Created Shadow Map with name', self.dtexture
        
    def transposeMatrix(self,mat):
        res = numpy.array([[0,0,0,0],
                           [0,0,0,0],
                           [0,0,0,0],
                           [0,0,0,0]],dtype=float)
        for i in xrange(4):
            for j in xrange(4):
                res[i][j] = mat[j][i]
        return res

    def invertCompareFunc(self):
        '''
        We dont want the shadows to be completely blank. 
        '''
        glReadPixelsi()
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FUNC,GL_GREATER)

    def resize(self):
        self.size = self.engine.win.h
        glBindTexture(GL_TEXTURE_2D,self.dtexture)
        glCopyTexImage2D(GL_TEXTURE_2D,GLint(0),GL_DEPTH_COMPONENT,GLint(0),GLint(0),self.size,self.size,GLint(0))

    def perspTransf (self):
        gluPerspective(self.fov,1,near,far)

        
    def lookAt(self):
         gluLookAt(self.pos[0],self.pos[1],self.pos[2],
                  self.look[0],self.look[1],self.look[2],
                  0,1,0)
        
    def genMap(self):    
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.fbo)

              
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.perspTransf()
        glViewport(0,0,self.size,self.size)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.pos = self.light.pos
        self.look = self.light.look
        self.lookAt()
        glClear(GL_DEPTH_BUFFER_BIT)
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(-10,1)
        self.engine.drawGeometry(1)
        glDisable(GL_POLYGON_OFFSET_FILL)
        glMatrixMode(GL_PROJECTION)
        glEnable(GL_TEXTURE_2D)
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)

    def genMatrix(self):        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        glPushMatrix()
        self.perspTransf()
        Pmatrix = glGetFloatv(GL_PROJECTION_MATRIX)
        glPopMatrix()
        
        gluPerspective(self.fov,self.engine.win.aspect,0.1,100)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glPushMatrix()
        #[-1,1] - > [0,1]
        glTranslatef(0.5,0.5,0)
        glScalef(0.5,0.5,1)
        #Plight
        glMultMatrixf(Pmatrix)
        #L**-1
        self.lookAt()
        #S(Plight)(l**-1)
        Mmatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        glPopMatrix()
        
        #=========Camera
        self.engine.gameCamera()
        #=====================      
        glTexGeni(GL_S,GL_TEXTURE_GEN_MODE,GL_EYE_LINEAR)
        glTexGeni(GL_T,GL_TEXTURE_GEN_MODE,GL_EYE_LINEAR)
        glTexGeni(GL_R,GL_TEXTURE_GEN_MODE,GL_EYE_LINEAR)
        glTexGeni(GL_Q,GL_TEXTURE_GEN_MODE,GL_EYE_LINEAR)
        
        Mmatrix = self.transposeMatrix(Mmatrix)
        
        glTexGenfv(GL_S,GL_EYE_PLANE,Mmatrix[0])
        glTexGenfv(GL_T,GL_EYE_PLANE,Mmatrix[1])
        glTexGenfv(GL_R,GL_EYE_PLANE,Mmatrix[2])
        glTexGenfv(GL_Q,GL_EYE_PLANE,Mmatrix[3])
        
        glEnable(GL_TEXTURE_GEN_S)
        glEnable(GL_TEXTURE_GEN_T)
        glEnable(GL_TEXTURE_GEN_R)
        glEnable(GL_TEXTURE_GEN_Q)


if __name__ == '__main__':
    from main import *
