import sys
from game import *
from tga import *
import highscores
class Menu(Interface):
    '''
    @requires: Game
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

        self.playerName = ""

        #Allocate resources
        #--- we do it in a temporary display func so that we can
        #--- show a load screen.
        self.display = self.displayMenu
        self.keyboard = self.menuKeyboard
        def tmp_display ():
            self.loadingScreen()
            self.game = Game(self)
            self.getGlutControl()
            glutDisplayFunc(self.display)
        glutDisplayFunc(tmp_display)
        music.new_music("media/pycave.mp3")
        music.play()

        glutMainLoop()

    def menuControl ( self):
        self.keyboard = self.menuKeyboard
        self.display = self.displayMenu
        self.getGlutControl()

    def loadingScreen (self):
        self.clearGL()
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
            if highscores.checkNewScore(score):
                self.display = self.askNameDisplay
                self.score = score
                self.keyboard = self.askNameKeyboard
        else:
            pass #User quit the game. No highscore submission.

        self.count +=1
        
    def clean(self):
        print 'You played', self.count, 'times'
        sys.exit()
        
    #===========================
    # Glut callbacks
    #==========================
    #TODO: Display options!
    def clearGL (self):
        glClearColor(1,1,1,1)
        
        glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_DEPTH_BUFFER_BIT)

    def displayMenu(self):
        self.clearGL()
        
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

    def askNameDisplay (self):
        """"""
        self.clearGL()
        glPushMatrix() 
        glTranslatef(-1,0,0)
        glScalef(0.0006,0.0006,0)
        glutils.drawString("Please insert your name:")
        glPopMatrix()
        glPushMatrix() 
        glTranslatef(-1,-0.2,0)
        glScalef(0.0006,0.0006,0)
        glutils.drawString(self.playerName)
        glPopMatrix()
        glutSwapBuffers()
        
    def menuKeyboard(self,key,x,y):        
        Interface.keyboard(self, key, x, y)
        key = key.lower()
        print ord(key)
        if key == 's' or ord(key) == 13:
            self.startGame = True
            
    def askNameKeyboard (self, key, x, y):
        if ord(key) == 13: #Enter
            highscores.maybeStore(self.playerName,self.score)
            self.menuControl() 
            return
        if ord(key) == 8: #delete key
            self.playerName = self.playerName[0:-1]
            return
        if ord(key) == 0x1b: #exit
            self.menuControl()
           
        self.playerName+=key
        
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
