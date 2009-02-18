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


from gameplay import *
from lighting import *
from OpenGL.GL import *
from sprite import *
import camera

class Game(Gameplay):
    '''
    @requires: Gameplay
    @summary: Gameplay plus lighting and rendering.
    '''
    def __init__(self,menu):
        '''
        We need a reference to a menu so we can give 
        GLUT control back to it when we are done.
        '''
        Gameplay.__init__(self)
        
        self.menu = menu
        #LIGHTING =========== 
        self.shadowDebug = False#True
         
        glEnable(GL_LIGHTING)
        self.enable_shadows = True
        #(-60, 70, -210), 
        self.light = Light(self, (1, 1, 1, 1), (-20, 0,-120,1), GL_LIGHT0, self.enable_shadows)
        
        if self.enable_shadows and self.light.shadowMap.disabled:
            print "Warning: Disabling shadows" 
            self.enable_shadows = False
            
        self.light.look = (0, 0, 50)
        self.ambientLight = Light(self, (1, 1, 1, 1), (0,50,30,1), GL_LIGHT1, False)
        self.backLight = Light(self,(0.2,0.2,0.2,1),(-10,-50,-30,1), GL_LIGHT2,False)
        
        self.ambientLight.on()
        self.light.on()
        self.backLight.on()

        if self.shadowDebug:
            self.perspTransf = self.light.shadowMap.perspTransf
            self.lookAt = self.light.shadowMap.lookAt
        else:
            self.perspTransf = lambda : gluPerspective(60,self.win.aspect,0.1,1500)
            self.lookAt = self.gameCamera        
        #=========
        
        #FOG ================
        glEnable(GL_FOG)
        fogColor = (0.3, .3, 0.3)
        fogMode = GL_EXP2
        glFogi(GL_FOG_MODE, fogMode)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, 0.004)
        glFogf(GL_FOG_START, 600.0)
        glFogf(GL_FOG_END, 1000.0)
        #=========================
        
        glEnable(GL_DEPTH_TEST)
        self.backgroundTone = 0.2
        
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
                
    def drawGeometry(self,mode):
        '''
        @param mode:
            0 - All
            1 - Shadow Casters
        '''
        
        renderingShadowCasters = mode == 1
        
        if not renderingShadowCasters:
            glDisable(GL_CULL_FACE)
        
        else:
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
        
        glActiveTexture(GL_TEXTURE0)
        self.tunnel.drawObstacles()

        if not renderingShadowCasters:
            self.tunnel.draw()

        # SOLID TEXTURED Casters==================
        glActiveTexture(GL_TEXTURE1)
        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LINE_SMOOTH)
        self.ship.draw()
        # Translucent textured stuff===
        
        # Translucent textured non-shadow-casters==
        if not renderingShadowCasters:
            self.ship.drawSmoke()

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glActiveTexture(GL_TEXTURE0)
        #=================================
        
    def gameCamera(self):
        gluLookAt(camera.pos[0],camera.pos[1],camera.pos[2] #-50
                ,camera.lookat[0],camera.lookat[1],camera.lookat[2]
                ,camera.normal[0],camera.normal[1],camera.normal[2]) 

    def renderFromEye(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,self.win.w,self.win.h)
        glLoadIdentity()
        
        self.perspTransf()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.lookAt()
        self.drawGeometry(0)

    def reshape(self,w,h):
        Gameplay.reshape(self, w, h)
        if self.enable_shadows:
            self.light.shadowMap.resize()
    
    def display(self):
        glClearColor(self.backgroundTone, self.backgroundTone, self.backgroundTone, 0.0)
        if profiling:
            cProfile.runctx('for x in xrange(10): self.render();',globals(),locals(),'prof')
        else:
            self.render()

    def renderScore (self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glPushMatrix()
        glColor4f(1,1,1,1)
        glTranslatef(0.5,0.8,0)
        glScalef(.0006,.0006,0)
        glutils.drawString("Score: " +  str(int(self.score))) #+" "+str(self.fps))
        glPopMatrix()
        if self.hardcore:
            glPushMatrix()
            glTranslatef(-0.55,-0.6,0)
            glScalef(0.001,0.001,0)
            glutils.drawString("HARDCORE MODE")
            glPopMatrix()
        
        
    def render(self):    
        if self.enable_shadows:
            glBindTexture(GL_TEXTURE_2D,self.light.shadowMap.dtexture)
            self.light.shadowMap.genMap()
            self.light.shadowMap.genMatrix()
            
        self.renderFromEye()
        self.renderScore()
        glutSwapBuffers()
    
    def idle(self):
        Gameplay.idle(self)
        glutPostRedisplay()
        if self.died == True:
            self.clean()

    def clean(self):
        '''
        '''
        Gameplay.clean(self)
        self.menu.gameEnded(self.score,self.died)#self.died may be false if user quit
        self.menu.getGlutControl()


if __name__=='__main__':
    from main import *
