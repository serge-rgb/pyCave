# -*- coding: utf-8 -*-
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


#tga.py, by Sergio González, 2007
#Class that loads TGA textures and can upload them into OpenGL

from OpenGL.GL import *
import struct

#Only loads 24 or 32 bit uncompressed TGA textures
#Use textures with powers of two dimensions on older hardware..
class TgaTexture:
	def __init__(self,fname):
		f = open(fname,'rb')
		
		#Skip useless stuff
		f.seek(12)
		
		w = struct.unpack('h', f.read(2))
		h = struct.unpack('h', f.read(2))
		bpp = struct.unpack('B', f.read(1))
		descriptor = f.read(1)
		
		self.size = (w[0],h[0])
		self.bpp = bpp[0]
		
		#Tga format stores it as BGR.
		#Let OpenGL do the changing.
		if self.bpp == 24:
			self.internFormat = 3
			self.texFormat = GL_BGR
		if self.bpp == 32:
			self.internFormat = 4
			self.texFormat = GL_BGRA
		else:
			print "Image Format not supported"
			exit(-1)
		 
		pixnum = self.size[0] * self.size[1]
		imgSize = pixnum * self.internFormat
		self.texels = f.read(imgSize)
		
		f.close()
		print 'TGALOADER: Loaded', self.bpp, 'bit,',self.size[0],'x',self.size[1],'image:',fname
		
	def newGLTexture(self):
		#self.name = name
		#glPixelStorei(GL_PACK_ALIGNMENT,1)
		self.name = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D,self.name)
		
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		
		glTexImage2D(GL_TEXTURE_2D, 0,self.internFormat,self.size[0],self.size[1],0,self.texFormat,GL_UNSIGNED_BYTE,self.texels)
		print 'TGALOADER: Stored 2D texture in OpenGL with name', self.name
		
		
		
