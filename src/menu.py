from renderer import Renderer
from interface import *
from tga import TgaTexture
import highscores
import glutils
import time
import music
from decorators import callparent

def displayFullWindowTexture(texture):
    '''
    texture is a TgaTexture with a gl texture
    associated. (i.e. texture.name is a GLInt texture name)
    Will fill the screen with the texture
    '''
    
    glutils.clearGL()

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE1)
    glBindTexture(GL_TEXTURE_2D,texture.name)

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
    glEnable(GL_TEXTURE_2D)
    glutSwapBuffers()
        #menu.game.getControl()

def checkButtons(buttons,coordx,coordy):
    '''
    Recieves a list of buttons.
    A button is a tuple containing:
    0: point (x,y), the up-left corner.,
    1: _x, the right-most x value 
    2:  _y, the lowest y value.
    3: a function to execute when clicked
    '''
    #problem: original button coordinates were thought
    #for 1024x540 window resolution.
    #Everything is screwed when window is maximized
    #quick-fix: convert any coordinate to a 1024x540
    #base
    ratiox = float(1024)/context.w
    ratioy = float(540)/context.h
    coordx*=ratiox
    coordy*=ratioy
    for b in buttons:
        (x,y) = b[0]
        _x = b[1]
        _y = b[2]
        func = b[3]
        if x<=coordx<=_x and y<=coordy<=_y:
            func()

class LoadingScreen (Frame):
    def __init__ (self,menu):
        self.menu = menu
        self.getControl ( )
        
    def display(self):
        glutils.clearGL()
        glutils.drawString("Loading...")
        glutSwapBuffers()
        
    def idle (self):
        'Idle, make the menu load the game'
        self.menu.loadGame ()
        self.menu.getControl()

class HelpScreen(Frame):
    def __init__(self,parent):
        self.parent = parent
        self.texture = TgaTexture("media/pyCaveHelp.tga")
        self.texture.newGLTexture()
        self.buttonList = [
            ((320,430),         #Exit to menu
             694,
             470,
             self.parent.getControl)]
        
    def display(self):
        displayFullWindowTexture(self.texture)        
        
    def keyboard(self,key,x,y):
        if ord(key) == 27: #Escape
            
            self.parent.getControl()
    @callparent(Frame)            
    def mouse(self,button,st,x,y):
        if st == GLUT_UP:
            checkButtons(self.buttonList,x,y)

    def idle(self):
        glutPostRedisplay()

class HighScores(Frame):
    def __init__(self,parent,):
        self.parent = parent
        self.currscore = 0
    def display(self):
        glutils.clearGL()
        if self.currscore != 0:
            glutils.drawString("Your score: "+str(int(self.currscore)),
                               translate=(0,0.8),
                               scale=1)
        
        glutils.drawString("Highscores:  (Press Esc to continue)",
                           translate=(0,0.6))
        glutSwapBuffers()
        
        def showElem (i,offset,elem):
            glPushMatrix() 
            glutils.drawString(str(i) + '- ' + elem.name + ":   " + str(int(elem.score)),
                               translate=(0.4,offset),
                               scale=0.8)
            glPopMatrix()
        offset = 0.4
        i = 1
        for elem in reversed(highscores.load()):
            showElem(i,offset,elem)
            offset-=0.1
            i+=1
        glutSwapBuffers()
        
    def keyboard(self,key,x,y):
        if ord(key) == 27:
            self.parent.getControl()

    def idle(self):
        pass
    #glutPostRedisplay()
     #   time.sleep(0.1)

class AskName(Frame):
    def __init__(self,parent,score=0):
        self.playerName = ''
        self.score = score
        self.parent = parent
        
        self.hsFrame = HighScores(self.parent)
        hs = highscores.load()
        
    def askOrShowHighscores(self,score):
        self.score = score
        hs = highscores.load()
        iscandidate = highscores.isCandidate(hs,score)
        if iscandidate:
            self.getControl()
        else:
            self.hsFrame.currscore=0
            self.hsFrame.getControl()
        
    def display (self):
        
        glutils.clearGL()
        glutils.drawString('Congratulations! You made top 10.',translate=(0,0.2))
       
        glutils.drawString("Please insert your name (or press Esc):")
        
        glutils.drawString(self.playerName,translate=(0,-0.2))
        glutSwapBuffers()
        
    def exitToHighscores(self):
        self.hsFrame.getControl()
        
    def keyboard (self, key, x, y):
        if ord(key) == 13: #Enter
            if self.playerName!="":
                highscores.maybeStore(self.playerName,self.score)
            self.hsFrame.currscore = self.score
            self.exitToHighscores()
                
        if ord(key) == DELETE_KEY: #delete key (8 in linux)
            self.playerName = self.playerName[0:-1]
            return
        if ord(key) == 0x1b: #exit
            self.hsFrame.currscore = 0
            self.exitToHighscores()
        self.playerName+=key
        self.playerName = self.playerName.strip()
        
    def idle(self):
        glutPostRedisplay()
        

class Menu(Frame):
    """
    DOC
    """
    def __init__(self):
        self.game = None #
        self.playCount = 0
        #Make the loading screen call loadGame for us
        loadscreen = LoadingScreen (self)
        self.logo = TgaTexture("media/pyCaveMenu.tga")
        self.logo.newGLTexture()

        music.new_music("media/pycave.mp3")
        music.play()
        if pyCaveOptions['mute']:
            music.mute()
        #MENU ITEMS------------------------------
        self.helpMenu= HelpScreen(self)
        self.hscores = HighScores(self)
        self.asker = AskName(self)
        
        self.buttonList = [
            ((133,166), #Start
             362,
             201,self.startGame),
            ((129, 239), #Help
             201,
             279,self.helpMenu.getControl),
            ((128, 321), #Mute
             316,
             353,self.toggleMute),
            ((129, 395), #Exit
             199,
             429,exit),
            ((129,470),#highscores
             293,
             505,self.hscores.getControl)
            ]
        
    def loadGame (self):
        self.game = Renderer(self)

    def startGame(self):
        self.playCount+=1
        music.stop()
        self.game.gameplay.clean()
        self.game.gameplay.start()
        self.game.getControl()
        
        
    def toggleMute(self):
        music.mute()
        
    def display(self):
        displayFullWindowTexture(self.logo)
        glutSwapBuffers()

    def keyboard(self,key,x,y):
        if ord(key) == 27: #esc
            if self.game.gameplay.playing:
                if self.game.gameplay.paused:
                    self.game.gameplay.togglePause()
                music.stop()
                self.game.getControl()
            else: #Not playing and pressed esc
                print 'You played',self.playCount,'times.'
                exit()
            
    def mouse(self,button,st,x,y):
        if st == GLUT_UP:
            checkButtons(self.buttonList,x,y)
        if pyCaveOptions['debug']:
            pass

    def getControl(self):
        Frame.getControl(self)
        glutPostRedisplay()
        music.play()
                
    def idle(self):
        glutPostRedisplay()
        
                
        


        
    

        
