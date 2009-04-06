#!/usr/bin/env python
# encoding: utf-8
"""
poc.py

Proof Of Concept of the 'interface' abstraction layer
"""
from interface import *
#from interface import context
import sprite
import lighting
#import gameplay
    
class DrawTest (Frame):
    def __init__(self):
        self.rot = 0.01
        self.light = lighting.Light (None,(1,1,1,1),
                                     (0,2,0),
                                     (1,0,0),
                                     GL_LIGHT0,True)
        #0,5,0   near 0.1 far 5
        self.light.configureShadowMap (60,0.5,2)
        self.light.on()
        self.spr = sprite.Sprite (0.02)
        self.spr.newTexture ("smoke.tga")
#        self.gameplay = gameplay.Gameplay (self)
        pass



    def display(self):
        if pyCaveOptions ['shadows'] and self.light.casts_shadows:
            self.light.shadowMap.genMap(self.drawGeometry)
            self.light.shadowMap.genMatrix(self.camera)
            pass
        else:
            glActiveTexture (GL_TEXTURE0)
            glDisable (GL_TEXTURE_2D)
        self.render ()
        glutSwapBuffers ()


    def camera(self):
        """
        """
        gluLookAt (-1,0,-1,
                        0,0,0,
                        0,1,0)

    def render(self):
        ext.fb_obj.glBindFramebufferEXT(ext.fb_obj.GL_FRAMEBUFFER_EXT,0)

        glViewport(0,0,context.w,context.h)
        #Clear everything
        #glClearColor(0,0,0,0)
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #-----------------------------------------------------------
        #Projection matrix
        #------------------------------------------------------------
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity ()
        gluPerspective (60,context.aspect (),0.001,2)

        #------------------------------------------------------------
        #Modelview matrix
        #------------------------------------------------------------
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()

        self.camera () #lookat
        self.drawGeometry ()
        
        
    def drawGeometry(self):
        """
        Send geometry to opengl
        """
        #------------------------------
        # Solid non-textured
        #------------------------------
        #DEACTIVATE TEX 1 (color)
        glActiveTexture (GL_TEXTURE1)
        glDisable (GL_TEXTURE_2D)

        #Draw a rotating cube
        glPushMatrix ()
        glTranslatef (0,0,0)
        glRotatef (self.rot,0.5,1,0)
        glutSolidCube(0.3)
        glPopMatrix ()

        
        #Draw Plane
        glPushMatrix()
        glTranslatef (0,-0.3,0)
        glScalef (1,0.05,1)
        glutSolidCube (1)
        glPopMatrix()

        #REACTIVATE COLOR TEX 1 
        glActiveTexture (GL_TEXTURE1)
        glEnable(GL_TEXTURE_2D)
        #------------------------------
        #Translucent non-casters
        #------------------------------        
        glActiveTexture (GL_TEXTURE0)
        glDisable (GL_TEXTURE_2D)
        glActiveTexture (GL_TEXTURE1)
        #Sprite
        glPushMatrix()
        glTranslatef (0,0.5 ,-0.2)
        self.spr.rotate =self.rot*2
        self.spr.draw ()
        glPopMatrix()

        glActiveTexture (GL_TEXTURE0)
        glEnable(GL_TEXTURE_2D)


    def keyboard (self):
        pass
    
    def idle (self):
        self.rot += 0.1
        glutPostRedisplay ()
        
frame = DrawTest ()
frame.getControl()

def go ():
    context.mainLoop ()
    
if __name__ == '__main__':
    go ()
