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
        glEnable(GL_LIGHTING)
        self.enable_shadows = True
        self.light = Light(self, (0, 1, 1, 0), (-20, 0, -120), 
                           GL_LIGHT0, True)
        if self.light.shadowMap.disabled:
            print "WARNING: Could not find Depth Texture extensions. Disabling lighting" 
            self.enable_shadows = False
            glDisable(GL_LIGHTING)

        self.light.look = (0, 0, 50)
        self.ambientLight = Light(self, (1, 1, 1, 1), (-20, 0,-120), 
                                  GL_LIGHT1, False)
        self.light2 = Light(self, (1, 1, 1, 0), (10, 10, 0), 
                           GL_LIGHT2, False)
        self.ambientLight.on()
        self.light.on()
        self.light2.on()
        #=========
        
        #FOG ================
        glEnable(GL_FOG)
        fogColor = (0.0, 0.0, 0.0)
        fogMode = GL_EXP2
        glFogi(GL_FOG_MODE, fogMode)
        glFogfv(GL_FOG_COLOR, fogColor)
        glFogf(GL_FOG_DENSITY, 0.0042)
        glFogf(GL_FOG_START, 250.0)
        glFogf(GL_FOG_END, 1000.0)
        #=========================
        
        glEnable(GL_DEPTH_TEST)
        tone = 0.1
        glClearColor(tone, tone, tone, 0.0)
        #glClearColor(1.0, 1.0, 1.0, 0.0)
        
        
    def drawGeometry(self,mode):
        '''
        mode:
            0 - All
            1 - Shadow Casters
        '''
        
        glActiveTexture(GL_TEXTURE0)
        #Solid stuff
        
        7# TEXTURED STUFF==================
        glActiveTexture(GL_TEXTURE1)
        glEnable(GL_TEXTURE_2D)
        self.ship.draw()
        glDisable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        #=================================
        
        # NON-SHADOW NON-TEXTURED CASTERS
        if not mode == 1:
            self.tunnel.draw()

    def gameCamera(self):
        gluLookAt(-150,0,0 #-50
                ,0,0,100
                ,0,1,0) 

    def renderFromEye(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glViewport(0,0,self.win.w,self.win.h)
        glLoadIdentity()
        gluPerspective(60,self.win.aspect,0.1,1500)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        self.gameCamera()
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
            glBindTexture(t2d,self.light.shadowMap.name)
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
        No docs d00d.
        '''
        Game.clean(self)


if __name__=='__main__':
    from main import *
