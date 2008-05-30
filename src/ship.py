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


from model import *

class Ship(Model):
    '''
    Extends Model class to define the ship.
    '''
    def __init__(self,game):
        Model.__init__(self,'media/Hmodel.obj','media/model.tga')
        self.createDisplayList()
        self.game = game
        
        #Standard acceleration and velocity.
        self.accel = 100  # units / time^2
        self.vel = 50  # units / time

        self.pos = (0,10,0)

    
    def idle(self,diff):
        '''
        Move, self-rotate to look alive.
        '''
        self.fall(diff)
    
    def draw(self):
        Model.draw(self)

        
    def fall(self,deltatime):
        #Am I pressing space to lift up?
        thrusting = self.game.keyMap[ord(' ')] == 1
        
        deltavel = self.accel * deltatime
        deltadist = self.vel * deltatime
        
        self.pos = (self.pos[0], 
                    self.pos[1] + deltadist,
                    self.pos[2])
        
        if not thrusting:
            self.vel -= deltavel
        else:
            self.vel += deltavel

    def die(self):
        #Do dome cooooool explosions!!
        pass
            
    def clean(self):
        self.freeList()
