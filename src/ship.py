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
from sprite import *


fname = 'media/smoke.tga' #smoke texture

smokeScale = 0.6
transInterval = 100
scaleInterval = 2
rotateInterval = (2*3.14159)*3
scaleLimit = 2

class Ship(Model):
    '''
    Extends Model class to define the ship.
    '''
    def __init__(self,game):
        Model.__init__(self,'media/Hmodel.obj','media/model.tga')
        self.createDisplayList()
        self.game = game
        self.smoke = [] #List of smoke sprites.
        spr = Sprite(smokeScale)
        spr.newTexture(fname)
        self.image = spr.image
        self.smoke.append(spr)
        self.addSmoke()
        
        #Standard acceleration and velocity.
        self.accel = 100  # units / time^2
        self.vel = 50  # units / time

        self.pos = (0,10,0)

    
    def idle(self,diff):
        '''
        Move, self-rotate to look alive.
        '''
        self.smokeIdle(diff) 
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

    #Smoke stuff=======================

    def addSmoke(self):
        spr = Sprite(smokeScale)
        spr.setTexture(self.image)
        spr.ypos = self.pos[1]
        spr.trans = 5 
        self.smoke.insert(0,spr)
        
    def smokeIdle(self,diff):
        if self.smoke[0].trans >= 10:
            self.addSmoke()
        for spr in self.smoke:
            spr.trans += transInterval*diff
            spr.xpos -= transInterval*diff
            spr.scale += scaleInterval*diff
            spr.rotate += rotateInterval*diff
            if spr.scale >= scaleLimit:
                self.smoke.remove(spr)
                if len(self.smoke) == 0:
                    self.addSmoke()

    def drawSmoke(self):
        for spr in self.smoke:
            spr.draw()
