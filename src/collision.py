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


from ship import *
from tunnel import *

lastChecked = None

def checkTunnel(ship,tunnel):
    global lastChecked
    
    index = int(abs(tunnel.trans/tunnel.dz))
    ra = tunnel.rings[index-1]  #ring behind the ship
    rb = tunnel.rings[index]#in front of the ship
    dist = abs(tunnel.trans) - (tunnel.dz*index) #Distance from rb to the ship
    
    #Bounds
    upper = ra.rad + ra.pos[1] + ra.upperTan*dist
    lower = -ra.rad + ra.pos[1] + ra.lowerTan*dist
    if ship.pos[1] > upper or ship.pos[1] < lower:
        return (True,0)
    
      #Now we check for an obstacle
    bonus = 0
    if hasattr(tunnel.rings[index],'obstacle'):
        pos = ship.pos
        obs = tunnel.rings[index].obstacle
        zObs = (index+1) * tunnel.dz
        zShip = -tunnel.trans
        y2 = abs(obs.y/2.0)
        disc = zObs - zShip
        if disc < obs.z: #within z-range
            if abs(obs.height - pos[1]) < y2: #within Y-range
                return (True,0)
            
        if lastChecked!=rb and abs(obs.height - pos[1]) < 20:
           bonus=100
           lastChecked=rb

    lastChecked = rb
    return (False,bonus)

if __name__ == '__main__':
    from main import *
    


