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



import math
import random
from OpenGL.GL import *
from OpenGL.GLUT import *

#Default vertices per ring
vertNum = 20

class Obstacle:
    def __init__(self,parent):
        self.parent = parent
        rad = int(round(parent.rad))
        self.height = random.randint(-rad,rad)
        #Size
        self.x = self.z = 5 #right now z has to be <= Tunnel.dz*2
        self.y = 40

    def draw(self):
        glPushMatrix()
        glTranslatef(0,self.height,self.parent.pos[2] - self.z/2)
        glScalef(self.x,self.y,self.z)
        #glutWireCube(1)
        glutSolidCube(1)
        glPopMatrix()

class Ring:
    '''
    The tunnel is composed of this rings.
    '''
    def __init__(self,rad,pos):
        self.rad = rad
        self.pos = pos
        self.verts = self.genVerts()
        self.lowerTan = 1
        self.upperTan = 1  #Tangent, the slope to the next ring. 
                        #Used for linear interpolation during collision detection
    def genVerts(self):
        res = []
        for i in xrange(vertNum+1):
            v = (self.rad * math.sin(math.pi* i / vertNum)+self.pos[0],
                 self.rad * math.cos(math.pi* i / vertNum)+self.pos[1],
                 self.pos[2])
            res.append(v)
        return res

    def addObstacle(self):
        self.obstacle = Obstacle(self)

class Tunnel:
    def __init__(self):
        #TODO: Change this to an array to save memory?
        self.rings = []
        self.maxRad = 40
        self.minRad = 30
        self.minOffset = -10
        self.maxOffset = 10
        self.scale = 2.0
        self.sineScale = 0.04
        self.sineOffset = 30
        self.currRing = 0
        
        #Position of new ring
        self.pos = (0,0,0)
        #The speed by which the tunnel gets smaller
        self.red = 0.005
        #The speed by which it moves (units per sec)
        self.vel = 55
        #How far apart are the rings
        self.dz = 20
        #Display list
        self.list = 0
        #Obstacle dList
        self.objlist=0
        #Translation in Z
        self.trans = -20
        
    def move(self,time):
        self.trans -= self.vel * time
        
    def newRing(self):
        rad = random.randrange(self.minRad,self.maxRad)
        off = random.randrange(self.minOffset,self.maxOffset)
        
        self.scale -= self.red
        rad *= self.scale

        self.pos = ( 0, off , self.pos[2] + self.dz)
        a = (self.pos[2] * self.sineScale) % (2*math.pi)
        b = math.sin(a)
        self.pos = (self.pos[0],self.pos[1] + b*self.sineOffset ,self.pos[2] )
        ring = Ring(rad,self.pos)
        prevIndex = len(self.rings) -1
        if prevIndex > 0:
            prev = self.rings[prevIndex]
            aU = ring.pos[1] + ring.rad - (prev.pos[1] + prev.rad)
            aL = ring.pos[1] - ring.rad - (prev.pos[1] - prev.rad)
            b = self.dz
            tanU = float(aU)/b
            tanL = float(aL) /b
            #ring.tan = tan
            prev.upperTan = tanU
            prev.lowerTan = tanL
            self.rings[prevIndex] = prev
        
        if len(self.rings) % 7 == 0 and len(self.rings)!= 0:
            ring.addObstacle()
        try:    
            del self.rings[self.currRing].verts
            del self.rings[self.currRing]
        except:
            #No problem if it was empty
            pass
        self.rings.insert(self.currRing,ring)
        self.currRing+=1
#        self.rings.append(ring)


    def draw(self):
        glMaterialfv(GL_FRONT,GL_DIFFUSE,(.9,.98,1,1))
        glMaterialfv(GL_BACK,GL_DIFFUSE,(0,0,0,1))
        
        glEnable(GL_NORMALIZE) #TODO: This is slow, fix...
        glPushMatrix()
        glTranslatef(0,0,self.trans)
        glCallList(self.list)
        glPopMatrix()
        glDisable(GL_NORMALIZE)
        glMaterialfv(GL_FRONT_AND_BACK,GL_DIFFUSE,(1,1,1,1))

    def drawObstacles(self):
        glPushMatrix()
        glTranslatef(0,0,self.trans)
        glCallList(self.objlist)
        glPopMatrix() 
    
    def createList(self):
    	'''
    	Just one display list for a tunnel with ~4000 triangles. Make
    	it more efficient?
    	'''
        print 'TUNNEL: Creating display list...'
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        glBegin(GL_QUADS)
        for i in xrange(len(self.rings) - 1):
            for j in xrange(vertNum):
                r1 = self.rings[i]
                r2 = self.rings[i+1]

                # x o-----------o w
                #   |           |
                #   |           |
                # y o-----------o z

                x = r1.verts[j]
                y = r1.verts[j+1]
                z = r2.verts[j+1]
                w = r2.verts[j]
                
                u = (x[0] - y[0], x[1] - y[1] , x[2] - y[2]) #x-y
                v = (z[0] - y[0], z[1] - y[1] , z[2] - y[2]) #z-y
                
                #Cross product normal
                #All quads in the Tunnel are coplanar
                n = (u[1]*v[2] - u[2]*v[1] , u[0]*v[2] - u[2]*v[0], u[0]*v[1] - u[1]*v[0])
                glNormal3fv(n)
                glVertex3fv(x)
                glVertex3fv(y)
                glVertex3fv(z)
                glVertex3fv(w)
        glEnd()

        glEndList()
        print 'Done.'

    def createObstacleList(self):
        self.objlist = glGenLists(1)
        glNewList(self.objlist,GL_COMPILE)

        for ring in self.rings:
            if hasattr(ring,'obstacle'):
                ring.obstacle.draw()
        glEndList()

    def clean(self):
        glDeleteLists(1,self.list)
        glDeleteLists(1,self.objlist)
        
    def clear(self):
        '''
        Delete all data in tunnel. (For usage when the game finishes
        and a new tunnel needs to be generated)
        '''
#        for ring in self.rings:
 #           del ring.verts[:]
  #      del self.rings[:]
        self.__init__()
        
if __name__=='__main__':
    from main import *
