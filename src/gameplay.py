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


from interface import *
from ship import *
from tunnel import *
import collision
import time

profiling = False

if profiling:
    import cProfile

class Gameplay(Interface):
    '''
    @requires: Interface
    @summary: Manages collisions, the ship, the cave, I/O
    '''
    def __init__(self):

        Interface.__init__(self)
        
        self.ship = Ship(self)
                
        #======================
        #TUNNEL
        self.tunnel = Tunnel()
        self.fillTunnel()
        #=======================        
        self.start()
        
    def start(self):
        self.cumTime = 0
        self.score = 0
        self.died = False 
        self.time = time.time()
        
        #Ascii keymap
        self.keyMap = []
        for i in xrange(0,256):
            self.keyMap.append(0)

    def fillTunnel(self):
        numRings = 370
        for i in xrange(numRings):  
            self.tunnel.newRing()
        len = self.tunnel.rings[numRings-1].pos[2]
        self.tunnel.createList()
        self.tunnel.createObstacleList()
        
    def keyboard(self,key,x,y):
        Interface.keyboard(self, key, x, y)
        self.keyMap[ord(key)] = 1
        
    def keyboardUp(self,key,x,y):
        self.keyMap[ord(key)] = 0
        
    def manageInput(self):
        pass
    
    def idle(self):
        '''
        '''
        self.manageInput()
        diff = time.time() - self.time
        crashed = collision.checkTunnel(self.ship,self.tunnel)
        if crashed:
            self.end()

        self.ship.idle(diff)
        self.tunnel.idle(diff)
        
        self.cumTime += diff
        self.time = time.time()
        
    def end(self):
        self.ship.die()
        self.died = True
        
    def clean(self):
        self.score = self.cumTime
        self.ship.reset()
        self.tunnel.reset()
        
if __name__ == '__main__':
    from main import *
                                                                           
