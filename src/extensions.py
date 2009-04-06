#!/usr/bin/env python
# encoding: utf-8
"""
extensions.py

Created by Sergio Gonzalez on 2009-03-20.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

from OpenGL import extensions as exts

#------------------------------
# Import extensions and add the modules to a list
#------------------------------
import OpenGL.GL.EXT.framebuffer_object as fb_obj
import OpenGL.GL.ARB.depth_texture as depth_texture
import OpenGL.GL.ARB.multitexture as multitext

extensions = [fb_obj , depth_texture, multitext]

hasExt = {} #Key: extension module. Value: Boolean

def printImportedExts ():
    print 'Imported extensions'
    try:
        for e in extensions:
            print e#,e.EXTENSION_NAME3
    except:
        exit(-1)
        
def checkExtensions():
    'Fill hasExt map with Booleans for each extension\'s availability '
    print 'Summary for Extensions:--------------------'
    for e in extensions:
        name = e.EXTENSION_NAME
        hasExt [e] = exts.hasGLExtension (name)
        print name, hasExt[e]
    print '------------------------------'

        
