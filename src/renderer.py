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


from game import *
from lighting import *
from OpenGL.GL import *
from sprite import *
import camera

class Renderer(Game):
    '''
    @requires: Game
    Game with lighting and rendering.
    '''
    def __init__(self):
        '''
        '''
        Game.__init__(self)
        

        #LIGHTING ===========
        self.shadowDebug = False#True
        glEnable(GL_LIGHTING)
        self.enable_shadows = True
        #(-60, 70, -210), 
        self.light = Light(self, (1, 1, 1, 1), (-100, 0,-120), 
                           GL_LIGHT0, self.enable_shadows)
        if self.enable_shadows and self.light.shadowMap.disabled:
            print "WARNING: Could not find Depth Texture extensions. Disabling shadows" 
            self.enable_shadows = False
            glDisable(GL_LIGHTING)
            
        self.light.look = (0, 0, 50)
        self.ambientLight = Light(self, (1, 1, 1, 1), (0,50,30), 
                                  GL_LIGHT1, False)
        self.backLight = Light(self,(0.2,0.2,0.2,1),(-10,-50,-30),
                               GL_LIGHT2,False)
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
        fogColor = (0.5, 0.5, 0.5)
        fogMode = GL_EXP
        glFogi(GL_FOG_MODE, fogMode)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, 0.0005)
        glFogf(GL_FOG_START, 250.0)
        glFogf(GL_FOG_END, 1000.0)
        #=========================
        
        glEnable(GL_DEPTH_TEST)
        tone = 0.1
        glClearColor(tone, tone, tone, 0.0)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        #glClearColor(1.0, 1.0, 1.0, 0.0)
        
        
    def drawGeometry(self,mode):
        '''
        mode:
            0 - All
            1 - Shadow Casters
        '''
       
        if not mode == 1:
            pass
            #glCullFace(GL_BACK)
            glDisable(GL_CULL_FACE)
        
        else:
            glEnable(GL_CULL_FACE)
            glCullFace(GL_FRONT)
        #    glEnable(GL_CULL_FACE)
            
        
        #glCullFace(GL_FRONT)
        glActiveTexture(GL_TEXTURE0)
        #Solid stuff
        self.tunnel.drawObstacles()
        # NON-SHADOW-CASTERS NON-TEXTURED 
        if not mode == 1:
            self.tunnel.draw()

        # SOLID TEXTURED Casters==================
        glActiveTexture(GL_TEXTURE1)
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        self.ship.draw()
        # Translucent textured stuff===
        
        # Translucent textured non-shadow-casters==
        if not mode ==1 or mode==1:
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
        Game.reshape(self, w, h)
        if self.enable_shadows:
            self.light.shadowMap.resize()
    
    def display(self):
        if profiling:
            cProfile.runctx('for x in xrange(10): self.render();',globals(),locals(),'prof')
        else:
            self.render()
                    
    def render(self):    
        if self.enable_shadows:
        #    glClear(GL_COLOR_BUFFER_BIT |  GL_DEPTH_BUFFER_BIT )
            glBindTexture(GL_TEXTURE_2D,self.light.shadowMap.dtexture)
            self.light.shadowMap.genMap()
            #TODO: Lots of rendering time is spent here. Optimize
            self.light.shadowMap.genMatrix()
            
        self.renderFromEye()
        glutSwapBuffers()
    
    def idle(self):
        Game.idle(self)
        glutPostRedisplay()
        if self.ended == True:
            self.clean() #This will change to something that returns to the menu

    def clean(self):
        '''
        '''
        Game.clean(self)


if __name__=='__main__':
    from main import *
