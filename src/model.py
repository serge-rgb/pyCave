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

from tga import *
from OpenGL.GLUT import*
		
class Model:
    def __init__(self,fname,texFile):
        self.mesh = OBJMesh(fname)
        self.pos = (0,0,0)
        self.rotate = (0,0,0)
        self.list = 0
        #self.createDisplayList()
        
        

        self.texFile = texFile
        if self.texFile != 'none':
                self.loadTexture(texFile)
                del self.texture.texels #We won't be needing this memory
                

		
    def createDisplayList(self):
        print 'MESH: Creating display list...'
        self.list = glGenLists(1)
        glNewList(self.list,GL_COMPILE)
        glBegin(GL_TRIANGLES)       
        for face in self.mesh.faces:
            for i in xrange(3):
                v = face[0][i]
                t = face[1][i]
                n = face[2][i]

                v = self.mesh.vertArray[v-1]
                t = self.mesh.textArray[t-1]
                n = self.mesh.normArray[n-1]

                glNormal3fv(n)
                glTexCoord2fv(t)
                glMultiTexCoord2fv(GL_TEXTURE1,t)
                if len(v) == 3: 
                    v.append(1)
                if len(v) == 4:
                    v[3] = 1
                glVertex4fv(v)
        glEnd()
        glEndList()
        print 'Done.'
        
    def freeList(self): 
	   	glDeleteLists(1,self.list)	
		
    def loadTexture(self,fname):
        self.texture = TgaTexture(fname)
        self.texture.newGLTexture()
		
    def draw(self):
        '''
        Must be drawn whene TEXTURE1 is active
        and TEXTURE_2D is enabled
        '''
        glBindTexture(GL_TEXTURE_2D,self.texture.name)
        glPushMatrix()

        glTranslatef(self.pos[0],self.pos[1],self.pos[2])
        glRotatef(self.rotate[0],1,0,0)
        glRotatef(self.rotate[2],0,0,1)  
        glCallList(self.list)
        #glutSolidSphere(1,10,10)
        glPopMatrix()
                
class OBJMesh:
    '''
    Reads .obj files containing vertex, texture coordinate and normal
    information. A non-compliant model will give ugly, uncatched
    exceptions.
    '''
    def __init__(self,fname):
        self.vertArray = []
        self.normArray = []
        self.textArray = []
        self.faces = []
        #For shadow volume calculation
        self.edges = [] 
        self.numFaces = 0
        self.openObjFile(fname)

    def openObjFile(self,fname):
        print 'MESH: Reading OBJ file...'
        f = open(fname,'rt')
        lines = f.readlines()
        f.close()
        words = []
        i = 0
        for line in lines:
            words = line.split()
            i += 1
            if len(words) < 1:
                continue
            if words[0] == 'v':
                x = float(words[1])
                y = float(words[2])
                z = float(words[3])
                self.vertArray.append([x,y,z]) 
            if words[0] == 'vt':
                u = float(words[1])
                v = float(words[2])
                self.textArray.append([u,v])
            if words[0] == 'vn':
                x = float(words[1])
                y = float(words[2])
                z = float(words[3])
                self.normArray.append([x,y,z])
            if words[0] == 'f':
                verts = []
                texcoords = []
                norms = []
                for w in words[1:]:
                    ind = w.split('/')
                    v = int(ind[0])
                    if(ind[1] != ''):
                        t = int(ind[1])
                    else:
                        t = 1
                    n = int(ind[2])
                    verts.append(v)
                    texcoords.append(t)
                    norms.append(n)	
                    self.faces.append( [verts,texcoords,norms] )
                    self.numFaces +=1
        print 'done.'
        print 'MESH: Loaded', len(self.vertArray), 'vertices,',len(self.textArray), 'texture coordinates and',len(self.normArray),'normals.'
        print 'Mesh has' , self.numFaces , 'faces.'
		
