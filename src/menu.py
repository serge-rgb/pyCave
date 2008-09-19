import sys
from game import *

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
        self.game = Game(self) #Allocate resources
        self.getGlutControl() #Snatch control
        glutMainLoop()        #Start everything

    def display(self):
        pass
    
    def keyboard(self,key,x,y):
        pass
    
    def idle(self):
        if not self.startGame:
            self.startGame = True
            self.game.getGlutControl()
        else:
            print 'Context!'
    
    
if __name__ == '__main__':
    from main import *