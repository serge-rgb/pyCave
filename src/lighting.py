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
from OpenGL.GLU import *
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

#less typing..
t2d = GL_TEXTURE_2D
near = 10
far = 500
class ShadowMap:
    def __init__(self,engine,light):
        self.fov = 60
        self.engine = engine
        self.size = engine.win.h
        self.name = glGenTextures(1)
        self.light = light
        self.disabled = False
        hasExt = glInitDepthTextureARB()
        if not hasExt:
            self.disabled = True
            return

        glBindTexture(t2d,self.name)
        glCopyTexImage2D(t2d,GLint(0),GL_DEPTH_COMPONENT,GLint(0),GLint(0),GLsizei(self.size),GLsizei(self.size),GLint(0))
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE) #CLAMP_TO_EDGE
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FUNC,GL_LEQUAL)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_MODE,GL_COMPARE_R_TO_TEXTURE)
        #Do this in a C module?..
        #c_module.setTexParamFailValue(0.5)
        #glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FAIL_VALUE,0.5)
        #glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_COLOR,0.5)
        #glTexParameteri(GL_TEXTURE_2D,GL_DEPTH_TEXTURE_MODE,GL_LUMINANCE)

        
        print 'SHADOW MAP: Created Shadow Map with name', self.name
        
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
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FUNC,GL_GREATER)

    def resize(self):
        self.size = self.engine.win.h
        glBindTexture(t2d,self.name)
        glCopyTexImage2D(t2d,GLint(0),GL_DEPTH_COMPONENT,GLint(0),GLint(0),self.size,self.size,GLint(0))
        
    def genMap(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov,1,near,far)
        glViewport(0,0,self.size,self.size)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPolygonOffset(1000,1000)
        self.pos = self.light.pos
        self.look = self.light.look
        gluLookAt(self.pos[0],self.pos[1],self.pos[2],
                  self.look[0],self.look[1],self.look[2],
                  0,1,0)
        
        self.engine.drawGeometry(1)
        
        glMatrixMode(GL_PROJECTION)
        glBindTexture(t2d,self.name)
        glCopyTexSubImage2D(t2d,0,0,0,0,0,self.size,self.size)
        glEnable(t2d)
        
    def genMatrix(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        glPushMatrix()
        gluPerspective(self.fov,1,near,far)
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
        gluLookAt(self.pos[0],self.pos[1],self.pos[2],
                  self.look[0],self.look[1],self.look[2],
                  0,1,0)
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
