#    This file is part of pyCave.
#
#    pyCave is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    pyCave is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with pyCave.  If not, see <http://www.gnu.org/licenses/>.


#from interface import *
import interface as intf
from ship import *
from tunnel import *
import collision
import time
import highscores
import glutils
    
profiling = False

if profiling:
    import cProfile

class HardcoreInterlude (intf.Frame):
    """
    Frame that waits for a while before loading HARDCORE MODE!
    """
    
    def __init__(self, parent):
        self.parent = parent
        self.getControl()
        self.init = time.time()
        self.limit = 1.3 #seconds
        
    def display(self):
        glutils.clearGL()
        glutils.drawString("Entering HARDCORE MODE")
        intf.glutSwapBuffers()
        intf.glutPostRedisplay()
    def idle(self):
        if time.time() - self.init >= self.limit:
            self.parent.gameplay.togglePause()
            self.parent.getControl()
        
class Gameplay():
    '''
    @summary: Manages collisions, the ship, the cave, I/O
    '''
    def __init__(self,renderer):
        self.renderer = renderer

        self.hardcoreLimit = 5500#100
        self.scorePerSecond = 10 #Each second merits 10 score.
        #------------------------------
        # Toggles
        #------------------------------
        self.hardcore = False
        self.paused = False
        self.playing = False
        
        #TODO: remove the horrible dependency on renderer
        self.ship = Ship(renderer)
        self.tunnel = Tunnel()
        
        self.start(); self.playing=False
        
    def start(self):
        self.score = 0
        self.paused = True
        self.died = False
        self.playing = True
        self.lastTime = time.time()
        self.elapsedTime = 0
        self.timePaused = 0
                
        
    def toHardcore (self):
        """"""
        interlude = HardcoreInterlude(self.renderer)
                
        self.hardcore=True
        self.tunnel.vel = 100
        self.scorePerSecond*=3
        self.paused=True

    def notHardcore (self):
        self.hardcore = False
        self.tunnel.vel = 55
        self.scorePerSecond=10

    def togglePause(self):
        if self.paused:
            self.lastTime = time.time()
            self.paused=False
            return
        self.paused=True
    
        
    def step(self):
        '''
        '''
        if self.paused:
            self.lastTime = time.time ()
            return
        startTime = time.time() 

        diff = time.time() - self.lastTime
        crashed = collision.checkTunnel(self.ship,self.tunnel)
        
        if crashed and intf.pyCaveOptions['mortal']:
            self.end()
            
        self.ship.idle(diff)
        self.tunnel.idle(diff)
        
        #======Enter hardcore mode when almost at the end.
        if not self.hardcore and self.tunnel.trans < -self.hardcoreLimit:
            
            self.toHardcore()
            self.tunnel.reset()
            self.ship.reset()
            
        self.score+=diff*self.scorePerSecond
        self.fps = 1/diff
        
        self.elapsedTime += diff
        self.lastTime = time.time()
        
    def end(self):
        '''
        Returns True if the player went into the highscore
        '''
        self.died=True
        self.playing = False
        self.ship.die()
        
    
    def clean(self):
        #Reset
        self.notHardcore()
        self.ship.reset()
        self.tunnel.reset()
        
if __name__ == '__main__':
    from main import *
                                                                           
