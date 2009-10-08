#!/usr/bin/env python
# encoding: utf-8
"""
interface.py

'Interface'  to GL,GLU and GLUT. Includes abstractions for
context and frames.
Frame is a class that can get control of input and display.


------------------------------
Usage
------------------------------
from interface import context,Frame

class MyFrame (Frame):
    display ():
        ...
    keyboard ():
        ...        
mf = MyFrame()
mf.getControl()

context.mainLoop()


------------------------------
Multitexturing convention
------------------------------
GL_TEXTURE0 is the shadow texture (Implement multiple shadowing?)
GL_TEXTURE1 is the color texture
"""
import os
DELETE_KEY = 127 if os.uname()[0]=='Darwin' else 8

pyCaveOptions = {
    'shadows':True,#False,
    'debug':False,#True
    'window_size':(1024,540),
    'show_fps':False,
    'mortal':True,#False
    'tunnel_geom':True,
    'mute':False,
    'cext_available':True
    }

import extensions as ext
import options

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

class Frame():
    """Can get control from GLUT and draw on screen / get keyboard input
    Override the keyboard(key),mouse(button,state,x,y), idle () and display() functions.
    Use getControl to do your stuff.
    """
    def keyboard(self, key,x,y):
        """
        Do something after receiving a key
        Arguments:   
        - `key`:
        """
        pass

    def keyboardUp (self,key,x,y):
        pass
    
    def display(self):
        '''Draw to screen'''
        pass
    
        
    def mouse(self,button,state,x,y):
        """handle mouse input"""
        if pyCaveOptions['debug']:
            if state == GLUT_UP:
                print x,y
        pass

    def passiveMotion(self,x,y):
        """
        Override to provide a callback for mouse movement
        (with no buttons pressed)
        """
        pass
    
    def idle(self):
        """
        Do stuff!
        """
        
        pass

    def getControl(self):
        """Be useful"""
        if pyCaveOptions ['debug']:
            print self, "Getting GLUT control"
        self.keyMap = []
        for i in xrange (0,256):
            self.keyMap.append (False)
        

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutKeyboardUpFunc (self.keyboardUp)
        glutMouseFunc(self.mouse)
        glutPassiveMotionFunc(self.passiveMotion)
        glutIdleFunc (self.idle)
        #TODO: add out of focus callback.
        glutPostRedisplay()
        
def checkFunctionality():
    'Redefine functions with GL extensions.'
    try:
        ext.checkExtensions()
    except AttributeError:
        print 'Error finding extension names. You probably don \'t have the latest version of pyOpenGL'
        exit ()
    
    #Checking for multitexture
    if not bool (glMultiTexCoord2f):
        if ext.hasExt[ext.multitext]:
            global glMultiTexCoord2fv,glMultiTexCoord2f,glActiveTexture,GL_TEXTURE0,GL_TEXTURE1
            glMultiTexCoord2f = ext.multitext.glMultiTexCoord2fARB
            glMultiTexCoord2fv = ext.multitext.glMultiTexCoord2fvARB
            glActiveTexture = ext.multitext.glActiveTextureARB
            GL_TEXTURE0 = ext.multitext.GL_TEXTURE0_ARB
            GL_TEXTURE1 = ext.multitext.GL_TEXTURE1_ARB
            if pyCaveOptions['debug']:
                print 'No multitexturing support. Importing extension'
                print 'Using ARB multitexturing'
        else:
            print 'No multitexturing functionality found. Exiting.'
            exit (-1)

    #Disable shadows if no extensions are available
    if not ext.hasExt[ext.fb_obj] or not ext.hasExt [ext.depth_texture]:
        print 'No Framebuffer Objects or Depth Texture extensions found.'
        print 'Disabling shadows'
        pyCaveOptions ['shadows']=False
    elif pyCaveOptions ['shadows']:
        ext.fb_obj.glInitFramebufferObjectEXT ()
        

def glSettings():
    """OpenGL state is configured here. 
    Every other glEnable called by a function ***MUST*** be
    followed by a glDisable ***WITHIN THE SAME FUNCTION***
    """

    glActiveTexture(GL_TEXTURE1)
    glTexEnvf (GL_TEXTURE_ENV,
               GL_COMBINE_RGB,
               GL_MODULATE)
    glEnable(GL_TEXTURE_2D)

    glActiveTexture(GL_TEXTURE0)
    glEnable(GL_TEXTURE_2D)
    
    glEnable(GL_LIGHTING)
    
    'Anti-aliasing'
    'TODO: hint opengl for AA quality?'    
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_LINE_SMOOTH)

    #Alpha blending
    glEnable(GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    #Depth-culling
    glEnable (GL_DEPTH_TEST)
    
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
    pass


class _Context():
    '''Thin abstraction over GLUT.'''
    def __init__(self, w,h,title):
        options.readOpts()
        
        if pyCaveOptions ['debug']:
            print 'New context object', self
            print 'Delete key is: ', DELETE_KEY
        print '''
        \n\n\n------------------------------
        Pycave\n------------------------------
        
        '''
        self.w = w
        self.h = h
        self.title = title
        glutInit()
        glutInitWindowSize (self.w,self.h)
        glutInitDisplayMode (GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH )
        
        # glClearStencil(0x1)  This generates a bug in Leopard 10.5!!
        # glutInitWindowPosition (win.x,win.y) Let the WM handle this

        glutCreateWindow(self.title)
        glutReshapeFunc(self.reshape)
        
        #Invoke the checking of extensions so that we can 
        #know what functionality to enable.

        checkFunctionality ()        
        glSettings()
        

    def aspect(self):
        """Get the aspect ratio"""
        return self.w / float(self.h)
        
    def reshape(self,w,h):
        self.w = w
        self.h = h
        glViewport(0,0,w,h)
    
    def mainLoop(self):
        """This calls the main loop. Never returns.
        Note: A Frame must request control before this is called.
        """
        glutMainLoop()        
context = _Context(pyCaveOptions ['window_size'] [0],
                   pyCaveOptions ['window_size'] [1],
                   "PyCave")
