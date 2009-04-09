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

#from OpenGL.GL import *
import interface as intf
from interface import pyCaveOptions
import struct

#Only loads 24 or 32 bit uncompressed TGA textures
#Use textures with powers of two dimensions on older hardware..
class TgaTexture:
	def __init__(self,fname):
		f = open(fname,'rb')
		
		#Skip useless stuff
		f.seek(12)
		
		(w,) = struct.unpack('h', f.read(2))
		(h,) = struct.unpack('h', f.read(2))
		(bpp,) = struct.unpack('B', f.read(1))
		descriptor = f.read(1)
		
		self.size = (w,h)
		self.bpp = bpp
		#Tga format stores it as BGR.
		#Let OpenGL do the changing.
		if self.bpp == 24:
			self.internFormat = 3
			self.texFormat = intf.GL_BGR
		if self.bpp == 32:
			self.internFormat = 4
			self.texFormat = intf.GL_BGRA
		elif self.bpp!=24 and self.bpp!=32:
			print "Image Format not supported", self.bpp,'@',self.size
			exit(-1)
		 
		pixnum = self.size[0] * self.size[1]
		imgSize = pixnum * self.internFormat
		self.texels = f.read(imgSize)
		f.close()
		if pyCaveOptions['debug']:
		    print 'TGALOADER: Loaded', self.bpp, 'bit,',self.size[0],'x',self.size[1],'image:',fname
		
	def newGLTexture(self):
		self.name = intf.glGenTextures(1)

		intf.glActiveTexture (intf.GL_TEXTURE1)
		
		intf.glBindTexture(intf.GL_TEXTURE_2D,self.name)
		
		intf.glTexParameteri(intf.GL_TEXTURE_2D, intf.GL_TEXTURE_WRAP_S, intf.GL_REPEAT)
		intf.glTexParameteri(intf.GL_TEXTURE_2D, intf.GL_TEXTURE_WRAP_T, intf.GL_REPEAT)
		intf.glTexParameteri(intf.GL_TEXTURE_2D, intf.GL_TEXTURE_MAG_FILTER, intf.GL_NEAREST)
		intf.glTexParameteri(intf.GL_TEXTURE_2D, intf.GL_TEXTURE_MIN_FILTER, intf.GL_NEAREST)
		intf.glTexImage2D(intf.GL_TEXTURE_2D,
				  0,self.internFormat,
				  self.size[0],self.size[1],0,
				  self.texFormat,intf.GL_UNSIGNED_BYTE,self.texels)
		if pyCaveOptions['debug']:
		    print 'TGALOADER: Stored 2D texture in OpenGL with name', self.name
			
