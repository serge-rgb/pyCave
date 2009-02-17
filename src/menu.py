import sys
from game import *
import music
import time

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
        self.game = Game(self) #Allocate resources
        self.getGlutControl()  #Snatch control
        music.new_music("media/pycave.mp3")
        music.play()
        glutMainLoop()

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
        glutSwapBuffers()
    
    def keyboard(self,key,x,y):        
        Interface.keyboard(self, key, x, y)
        key = key.lower()
        if key == 's':
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
    
    
if __name__ == '__main__':
    from main import *
