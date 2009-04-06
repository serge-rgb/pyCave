#!/usr/bin/env python
# encoding: utf-8
"""
poc.py

Proof Of Concept of the 'interface' abstraction layer
"""
import interface as intf
from interface import context
import sprite
import lighting
import gameplay
import highscores
import glutils

camera = {
    'pos':(-100,0,-90),
    'lookat':(0,0,90),
    'normal':(0,1,0)
    }

class Renderer (intf.Frame):
    def __init__(self,parent):
        self.parent = parent #The parent frame, a menu
        self.light = lighting.Light (None,(1,1,1,1),
                                     (-20,0,-120),
                                     (0,1,0),
                                     intf.GL_LIGHT0,True)
        #0,5,0   near 0.1 far 5
        self.light.lookAt (0,0,90)
        self.light.configureShadowMap (fov=60,near=110,far=200)
        self.light.on()
        
        self.gameplay = gameplay.Gameplay(self)
        self.gameplay.togglePause()
        
        #self.getControl ()
        
    def display(self):
        if self.gameplay.paused:
            glutils.clearGL()
            glutils.drawString ("Press p or click when you're ready.")
            intf.glutSwapBuffers()
            return

        if intf.pyCaveOptions ['shadows'] and self.light.casts_shadows:
            self.light.shadowMap.genMap(self.drawShadowCasters)
            self.light.shadowMap.genMatrix(self.camera)
            
        self.render ()
        self.renderText()
        intf.glutSwapBuffers ()

    def camera(self):
        'lookAt'
        pos = camera ['pos']
        lookat = camera ['lookat']
        normal = camera ['normal']
        intf.gluLookAt(pos[0],pos[1],pos[2] #-50
                       ,lookat[0],lookat[1],lookat[2]
                       ,normal[0],normal[1],normal[2]) 

    def render(self):
        intf.glViewport(0,0,context.w,context.h)
        #intf.glClearColor(0,0,0,0)
        intf.glClearColor(1,1,1,1)
        intf.glClear(intf.GL_COLOR_BUFFER_BIT | intf.GL_DEPTH_BUFFER_BIT)

        #-----------------------------------------------------------
        #Projection matrix
        #------------------------------------------------------------
        intf.glMatrixMode (intf.GL_PROJECTION)
        intf.glLoadIdentity ()
        intf.gluPerspective(60,context.aspect (),0.1,1500)

        #------------------------------------------------------------
        #Modelview matrix
        #------------------------------------------------------------
        intf.glMatrixMode (intf.GL_MODELVIEW)
        intf.glLoadIdentity ()

        self.camera () #lookat

        self.drawGeometry ()

        
    def drawGeometry(self):
        """
        Send geometry to opengl
        """
                
        intf.glActiveTexture (intf.GL_TEXTURE0)

        #UNTEXTURED
        intf.glActiveTexture (intf.GL_TEXTURE1)
        intf.glDisable (intf.GL_TEXTURE_2D)
        self.gameplay.tunnel.drawObstacles()
        self.gameplay.tunnel.draw ()
        intf.glEnable (intf.GL_TEXTURE_2D)

        #TEXTURED
        self.gameplay.ship.draw ()
                
        #SPRITES
        
        intf.glDisable (intf.GL_DEPTH_TEST)
        self.gameplay.ship.drawSmoke ()
        intf.glEnable (intf.GL_DEPTH_TEST)

        intf.glActiveTexture (intf.GL_TEXTURE0)
        intf.glEnable(intf.GL_TEXTURE_2D)

    def drawShadowCasters(self):
        """
        Some geometry
        """
        self.gameplay.tunnel.drawObstacles()
        self.gameplay.ship.draw ()
#        self.gameplay.ship.drawSmoke ()
        #self.gameplay.tunnel.draw ()

    def renderText (self):
        intf.glMatrixMode(intf.GL_MODELVIEW)
        intf.glLoadIdentity()
        intf.glMatrixMode(intf.GL_PROJECTION)
        intf.glLoadIdentity()
        
        glutils.drawString("Score: " +  str(int(self.gameplay.score)),
                           translate=(1.5,0.8))
        
        if intf.pyCaveOptions['show_fps']:
            glutils.drawString("FPS: " +  str(int(self.gameplay.fps)),
                               translate=(1.5,0.6))
            
        if self.gameplay.hardcore:
            glutils.drawString("HARDCORE MODE",translate=(0.45,-0.6),
                               scale = 2)
            
    def keyboard (self,key,x,y):
        self.keyMap[ord(key)]=True
        
        if intf.pyCaveOptions ['debug']:
            pass
        if key=='p':
            self.gameplay.togglePause ()
        if ord(key)==27:#esc
            if not self.gameplay.paused:
                self.gameplay.togglePause()
            self.parent.getControl()
            
    def keyboardUp (self,key,x,y):
        self.keyMap[ord(key)]=False

    def mouse(self,button,st,x,y):
        if st==intf.GLUT_UP:
            self.keyMap[ord(' ')]=False
        else:
            if self.gameplay.paused:
                self.gameplay.togglePause()
            else:
                self.keyMap[ord(' ')]=True
    
    def idle (self):
        self.gameplay.step()
        if self.gameplay.died:
            self.gameplay.clean()
            self.parent.asker.askOrShowHighscores(self.gameplay.score)
            
        intf.glutPostRedisplay ()
        
        
#frame = Renderer ()

def go ():
    context.mainLoop ()
    
if __name__ == '__main__':
    go ()
