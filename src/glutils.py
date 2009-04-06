import interface as intf

def drawString(text, scale=1.0,
               translate=(0,0),
               font=intf.GLUT_STROKE_ROMAN):##font=intf.GLUT_BITMAP_TIMES_ROMAN_24
    #disable texturing
    intf.glActiveTexture (intf.GL_TEXTURE1)
    intf.glDisable(intf.GL_TEXTURE_2D)
    intf.glActiveTexture (intf.GL_TEXTURE0)
    intf.glDisable(intf.GL_TEXTURE_2D)

    
    intf.glMatrixMode(intf.GL_MODELVIEW)
    intf.glPushMatrix()
    
    intf.glTranslatef(-1,0,0)
    intf.glTranslatef(translate[0],translate[1],0)
    
    
    intf.glScalef(0.0006,0.0006,0)
    intf.glScalef(scale,scale,0)
    
    for c in text:
        intf.glutStrokeCharacter(font,ord(c))

    intf.glPopMatrix()
    #reenable texturing
    intf.glEnable(intf.GL_TEXTURE_2D)
    intf.glActiveTexture (intf.GL_TEXTURE1)
    intf.glEnable(intf.GL_TEXTURE_2D)
        
                
def clearGL ():
    intf.glClearColor(1,1,1,1)        
    intf.glClear(intf.GL_COLOR_BUFFER_BIT)
    intf.glClear(intf.GL_DEPTH_BUFFER_BIT)
    intf.glMatrixMode (intf.GL_MODELVIEW)
    intf.glLoadIdentity ()
    intf.glMatrixMode (intf.GL_PROJECTION)
    intf.glLoadIdentity ()
    
        

    
