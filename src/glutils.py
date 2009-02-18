from OpenGL.GLUT import *
def drawString(text, font=GLUT_STROKE_ROMAN):#font=GLUT_BITMAP_TIMES_ROMAN_24):
    for c in text:
        glutStrokeCharacter(font,ord(c))
#        glutBitmapCharacter(font, ord(c))

    
