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
import interface as intf
try:
    import cext
except:
    print "Warning: no cext extension available. Startup time will be long."
    intf.pyCaveOptions['cext_available']=False

#Default vertices per ring
vertNum = 25#35

class Obstacle:
    '''
    @param parent: Ring
    '''
    def __init__(self,parent,scale,height):
        #x y z: Size
        self.x = self.z = 5*scale #right now z has to be <= Tunnel.dz*2
        self.y = 20*scale
        self.parent = parent
        diam = int(round(parent.rad)*scale/4)
        #height: position
        self.height = height + random.randint(-diam,diam)


    def draw(self):
        intf.glPushMatrix()
        intf.glTranslatef(0,self.height,self.parent.pos[2] - self.z/2)
        intf.glScalef(self.x,self.y,self.z)
        #intf.glutWireCube(1)
        intf.glutSolidCube(1)
        intf.glPopMatrix()

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

    def addObstacle(self,scale):
        self.obstacle = Obstacle(self,scale,self.pos[1])

class Tunnel:
    def __init__(self):
        self.numRings = 370
        self.rings = []
        self.maxRad = 40#40
        self.minRad = 30#30
        #Y-Offset of each ring's position
        self.minOffset = -10
        self.maxOffset = 10
        self.scale = 2.0
        #Scalars to control the sine wave that transforms the tunnel.
        self.sineScale = 0.04
        self.sineOffset = 30
        self.currRing = 0
        
        #Position of new ring
        self.pos = (0,0,0)
        #The speed by which the tunnel gets smaller
        self.red = 0.005
        #The speed by which it moves (units per second)
        self.vel = 55
        #How far apart are the rings
        self.dz = 20
        #Display list
        self.list = 0
        #Obstacle display list
        self.objlist=0
        self.reset()
        
        #Procedurally generate the tunnel:
        self.fill()

    def reset(self):
        #Translation in Z
        self.trans = -20
        
    def idle(self,time):
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
        
        #Add tangent information to the previous ring. Used in collision detection.
        if prevIndex > 0:
            prev = self.rings[prevIndex]
            #tangent := a/b.
            #aU upper a, aL lower
            aU = ring.pos[1] + ring.rad - (prev.pos[1] + prev.rad)
            aL = ring.pos[1] - ring.rad - (prev.pos[1] - prev.rad)
            b = self.dz
            #Upper tangent and lower tangent. 
            tanU = float(aU)/b
            tanL = float(aL) /b
            #ring.tan = tan
            prev.upperTan = tanU
            prev.lowerTan = tanL
            self.rings[prevIndex] = prev
        
        
        #Add an obstacle on a random basis
        if len(self.rings)% 10 == random.randint(0,9) and len(self.rings) > 5:
            ring.addObstacle(self.scale)

        try:    
            del self.rings[self.currRing].verts
            del self.rings[self.currRing]
        except:
            pass #No problem if it was empty
        self.rings.insert(self.currRing,ring)
        self.currRing+=1

    def fill(self):

        for i in xrange(self.numRings):  
            self.newRing()
        len = self.rings[self.numRings-1].pos[2]
        self.createList()
        self.createObstacleList()
        
    
    def draw(self):
        intf.glMaterialfv(intf.GL_FRONT,intf.GL_DIFFUSE,(.9,.98,1,1))
        intf.glMaterialfv(intf.GL_BACK,intf.GL_DIFFUSE,(0,0,0,1))
        
        intf.glEnable(intf.GL_NORMALIZE) #TODO: This is slow, fix...
        intf.glPushMatrix()
        intf.glTranslatef(0,0,self.trans)
        intf.glCallList(self.list)
        intf.glPopMatrix()
        intf.glDisable(intf.GL_NORMALIZE)
        intf.glMaterialfv(intf.GL_FRONT_AND_BACK,intf.GL_DIFFUSE,(1,1,1,1))

    def drawObstacles(self):
        intf.glPushMatrix()
        intf.glTranslatef(0,0,self.trans)
        intf.glCallList(self.objlist)
        intf.glPopMatrix() 

    def createList(self):
    	'''
    	Just one display list for a tunnel with ~4000 triangles. Make
    	it more efficient?
    	'''
#        print 'TUNNEL: Creating display list...'
        self.list = intf.glGenLists(1)
        intf.glNewList(self.list,intf.GL_COMPILE)
        intf.glBegin(intf.GL_QUADS)
        #intf.glBegin(intf.GL_LINE_STRIP)

        def diffVectors(x,y):
            return (x[0] - y[0], x[1] - y[1] , x[2] - y[2]) #x-y

        def cross(u,v):
            return (u[1]*v[2] - u[2]*v[1] , u[0]*v[2] - u[2]*v[0], u[0]*v[1] - u[1]*v[0])
        
        for i in xrange(len(self.rings) - 1):
            for j in xrange(vertNum):
                r1 = self.rings[i]
                r2 = self.rings[i+1]
                #             to--------o u
                #              |        |
                #              |        |
                # p o--------x o--------o w
                #   |          |        |  
                #   |          |        |  
                # q o--------y o--------o z
                
                #                        
                #   r0        r1        r2       r3
                #             

                x = r1.verts[j]
                y = r1.verts[j+1]
                z = r2.verts[j+1]
                w = r2.verts[j]
                try:
                    r0 = self.rings[i-1]
                    p = r0.verts[j]
                    q = r0.verts[j+1]
                except:
                    p = w
                    q = y
                    
                try:
                    t = r1.verts[j-1]
                except:
                    t = y
                try:
                    u = r2.verts[j-1]
                except:
                    u = z
                    
                    
                #Cross product normals
                if j==0:
                    nx =  cross(diffVectors(t,x),
                                diffVectors(p,x))
                    nw =  cross(diffVectors(u,w),
                                diffVectors(x,w))
                else:
                    nx =  cross(diffVectors(p,x),
                            diffVectors(t,x))
                    nw =  cross(diffVectors(x,w),
                                diffVectors(u,w))
                    
                ny = cross(diffVectors(q,y),
                          diffVectors(x,y))

                
                nz =  cross(diffVectors(y,z),
                            diffVectors(w,z))
                
                #TODO: This func. calls are the startup bottleneck:
                
                if intf.pyCaveOptions['tunnel_geom']:
                    if intf.pyCaveOptions['cext_available']:
                        cext.sendVertex(nx,x)
                        cext.sendVertex(ny,y)
                        cext.sendVertex(nz,z)
                        cext.sendVertex(nw,w)
                    else:
                        intf.glNormal3fv(nx)
                        intf.glVertex3fv(x)
                        intf.glNormal3fv(ny)
                        intf.glVertex3fv(y)
                        intf.glNormal3fv(nz)
                        intf.glVertex3fv(z)
                        intf.glNormal3fv(nw)
                        intf.glVertex3fv(w)
        intf.glEnd()
        intf.glEndList()
        

    def createObstacleList(self):
        self.objlist = intf.glGenLists(1)
        intf.glNewList(self.objlist,intf.GL_COMPILE)

        for ring in self.rings:
            if hasattr(ring,'obstacle'):
                ring.obstacle.draw()
        intf.glEndList()

    def clean(self):
        intf.glDeleteLists(1,self.list)
        intf.glDeleteLists(1,self.objlist)
        
    def clear(self):
        '''
        TODO: Delete this method? The tunnel is only generated once.
        '''
        pass
        
if __name__=='__main__':
    from main import *
