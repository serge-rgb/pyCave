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

#We are using so many GL calls it makes sense to import to global namespace
from interface import *

#WARNING -- To those who dare to change the parameters to the shadow map
# and to the position of the light variable on the Game class:
# ..
# It's almost impossible to get a better looking configuration for
# their parameters.

class Light:
    '''
    example: light((1,1,1,1) ,(10,0,1) ,GL_LIGHT0, True)
    '''
    def __init__(self, engine, color, pos,normal, num, casts_shadows):
        self.pos = pos
        self.normal = normal
        self.look = (0,0,0)
        
        self.color = color
        self.num = num
        self.casts_shadows = casts_shadows
        
        glLightfv(self.num, GL_POSITION, pos)
        glLightfv(self.num, GL_DIFFUSE, color)
        glLightfv(self.num, GL_SPECULAR, color)
#        glLightf (self.num, GL_SPOT_CUTOFF, 40.0)
        
        if self.casts_shadows and pyCaveOptions ['shadows']:
            self.shadowMap = ShadowMap(self)
        elif pyCaveOptions ['debug']==True:
            print self,": I dont have a texture map"
    
    def move(self, sum):
        self.pos = (self.pos[0] + sum[0] , self.pos[1]+sum[1], self.pos[2] + sum[2])
        self.look =(self.look[0] + sum[0] , self.look[1]+sum[1], self.look[2] + sum[2]) 
        glLightfv(self.num, GL_POSITION, self.pos)
    
    def on(self):
        glEnable(self.num)
    
    def off(self):
        glDisable(self.num)
    def configureShadowMap(self, fov,near,far):
        """
        Set values for the shadow map
        
        Arguments:
        - `fov`: field of view
        - `near`,`far`: ..
        """
        if not self.casts_shadows or not pyCaveOptions ['shadows']:
            return
        self.shadowMap.near = near
        self.shadowMap.far = far
        self.shadowMap.fov = fov
        
    def lookAt (self,x,y,z):
        self.look =(x,y,z)
    
class ShadowMap:
    def __init__(self,light):
        if pyCaveOptions ['debug']:
            print "SHADOW MAP", self
            
        self.near = 0.1
        self.far = 10
        self.fov = 60
        self.size = 512
        self.dtexture = glGenTextures(1)
        
        self.light = light
        self.fbo = 0
        glActiveTexture (GL_TEXTURE0)
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D,self.dtexture)
#        glTexImage2D (GL_TEXTURE_2D,0,GL_RGB,
#                      self.size,self.size,0,GL_RGB,GL_UNSIGNED_BYTE,None)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT ,
                     self.size, self.size, 0,GL_DEPTH_COMPONENT, GL_UNSIGNED_BYTE, None)

        texfilter = GL_LINEAR
#        texfilter = GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP_TO_EDGE) 
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, texfilter)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, texfilter)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_FUNC,GL_LEQUAL)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_COMPARE_MODE,GL_COMPARE_R_TO_TEXTURE)

        self.fbo = ext.fb_obj.glGenFramebuffersEXT(1)
        try:
            ext.fb_obj.glBindFramebufferEXT(ext.fb_obj.GL_FRAMEBUFFER_EXT,self.fbo)
        except Exception :
            print "Error binding framebuffer"
            print ext.fb_obj.GL_FRAMEBUFFER_EXT,self.fbo
            raise
            exit()
            
        ext.fb_obj.glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT,GL_DEPTH_ATTACHMENT_EXT,#GL_COLOR_ATTACHMENT0_EXT,
                                  GL_TEXTURE_2D,self.dtexture,0)
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)

        enum = ext.fb_obj.glCheckFramebufferStatusEXT(GL_FRAMEBUFFER_EXT)

        if enum == ext.fb_obj.GL_FRAMEBUFFER_COMPLETE_EXT:
            if pyCaveOptions ['debug']:
                print 'FRAMEBUFFER is COMPLETE'
        elif pyCaveOptions ['debug']:
            print "Framebuffer INCOMPLETE:"
            if enum == ext.fb_obj.GL_FRAMEBUFFER_INCOMPLETE_DIMENSIONS_EXT:
                print 'Dimension error'
            if enum == ext.fb_obj.GL_FRAMEBUFFER_INCOMPLETE_ATTACHMENT_EXT:
                print 'Attachment error'
            if enum == ext.fb_obj.GL_FRAMEBUFFER_INCOMPLETE_DRAW_BUFFER_EXT:
                print "incomplete draw buffer"
            if enum == ext.fb_obj.GL_FRAMEBUFFER_INCOMPLETE_READ_BUFFER_EXT:
                print "incomplete read buffer"
                
            if pyCaveOptions ['debug']:
                print 'FRAMEBUFFER_STATUS', enum
                exit ()
                
        ext.fb_obj.glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,0)
          
    def transposeMatrix(self,mat):
        res = [[0,0,0,0],
               [0,0,0,0],
               [0,0,0,0],
               [0,0,0,0]]
               
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
#        self.size = self.engine.win.h
        self.size = context.h
        
        glBindTexture(GL_TEXTURE_2D,self.dtexture)
        glCopyTexImage2D(GL_TEXTURE_2D,GLint(0),GL_DEPTH_COMPONENT,GLint(0),GLint(0),self.size,self.size,GLint(0))

    def perspTransf (self):
        gluPerspective(self.fov,1,self.near,self.far)

        
    def lookAt(self):
         gluLookAt(self.light.pos[0],self.light.pos[1],self.light.pos[2],
                   self.light.look[0],self.light.look[1],self.light.look[2],
                   self.light.normal[0],self.light.normal[1],self.light.normal[2])
        
    def genMap(self, drawCasters):
        """
        Generates shadow map.
        
        Arguments:
        - `drawCasters`: function that renders shadow casters
        """
        ext.fb_obj.glBindFramebufferEXT(GL_FRAMEBUFFER_EXT,self.fbo)

        glBindTexture(GL_TEXTURE_2D,self.dtexture)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.perspTransf()
        glViewport(0,0,self.size,self.size)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.lookAt()

        glClear(GL_DEPTH_BUFFER_BIT )
        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(-1,0)
        
        drawCasters() 

        glDisable(GL_POLYGON_OFFSET_FILL)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        ext.fb_obj.glBindFramebufferEXT(ext.fb_obj.GL_FRAMEBUFFER_EXT,0)
        pass
                

    def genMatrix(self,gameCamera):
        """
        Generates the transformation matrix for
        See paper:
        TODO: add paper reference
        Arguments:
        - `gameCamera`: Function that basically calls a gluLookAt
        """
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        glPushMatrix()
        self.perspTransf()
        Pmatrix = glGetFloatv(GL_PROJECTION_MATRIX)
        glPopMatrix()
        
        gluPerspective(self.fov,context.aspect(),0.1,100)
        
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
        gameCamera ()
        #=====================
        glActiveTexture (GL_TEXTURE0)
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

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()



if __name__ == '__main__':
    from main import *
