import sys
from game import *
from tga import *
class Menu(Interface):
    '''
    @requires: Game
    @summary: Extends Game to be controlled by a Menu.
    '''
    def __init__(self):
        '''
        We allocate resources for a new game. 
        However, we want to mantain control of the rendering
        context so we can display our menu.
        Eventually, we give control to Game to start playing.
        '''
        self.startGame = False
        
        #=======
        self.count = 0
        self.getGlutControl()  #Snatch control
        self.logo = TgaTexture("media/pycaveLogo.tga")
        self.logo.newGLTexture()

        #Allocate resources
        #--- we do it in a temporary display func so that we can
        #--- show a load screen.
        def tmp_display ():
            self.loadingScreen()
            self.game = Game(self)
            self.getGlutControl()
            glutDisplayFunc(self.display)
        glutDisplayFunc(tmp_display)
        music.new_music("media/pycave.mp3")
        music.play()

        glutMainLoop()

    def loadingScreen (self):
        glClearColor(1,1,1,1)
        glClear(GL_COLOR_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(-1,0,0)
        glScalef(0.0006,0.0006,0)
        glutils.drawString("Loading...")
        glPopMatrix()
        glutSwapBuffers()
        
    def gameEnded(self,score,died):
        '''
        @param ended: True: You died, False: You quit.
        '''
        if died:
            print "SCORE:",score
        else:
            print "You quit the game"
        
        self.count +=1
        
    def clean(self):
        print 'You played', self.count, 'times'
        sys.exit()
        
    #===========================
    # Glut callbacks
    #==========================
    #TODO: Display options!        
    def display(self):
        glClearColor(1,1,1,1)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

#        glViewport(0,0,1024,540)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        glDisable(GL_LIGHTING)

        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D,self.logo.name)

        glBegin(GL_QUADS)
        glMultiTexCoord2f(GL_TEXTURE1,1,1)
        glVertex3f(1,1,0)
        
        glMultiTexCoord2f(GL_TEXTURE1,1,0)
        glVertex3f(1,-1,0)

        glMultiTexCoord2f(GL_TEXTURE1,0,0)
        glVertex3f(-1,-1,0)

        glMultiTexCoord2f(GL_TEXTURE1,0,1)
        glVertex3f(-1,1,0)

        glEnd()

        glEnable(GL_LIGHTING)
        glutSwapBuffers()

    def keyboard(self,key,x,y):        
        Interface.keyboard(self, key, x, y)
        key = key.lower()
        print ord(key)
        if key == 's' or key == '\n':
            self.startGame = True

    def idle(self):
        if self.startGame:        
            self.startGame = False    
            self.game.getGlutControl()
            self.game.start()
            music.stop()
        else:
            music.play()
            time.sleep(0.02)
            pass
        glutPostRedisplay()
    
if __name__ == '__main__':
    from main import *
