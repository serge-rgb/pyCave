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

import pygame.mixer as mixer

mixer.init(44100,-16,6,3072)
mixer.music.set_volume(1.0)

def mute ():
	muted = mixer.music.get_volume()==0.0

	if not muted:
		mixer.music.set_volume(0.0)
	else:
		mixer.music.set_volume(1.0)
	
def new_music (music_file):
	""""""
	try:
		mixer.music.load(music_file)
	except:
		print "Error loading %s" % music_file
		raise SystemExit
		
	
def play():
	try:
		if not mixer.music.get_busy():
			mixer.music.rewind()
			mixer.music.play()			
	except:
		print "Error playing music"
		raise SystemExit
def stop ():
	""""""
	if mixer.music.get_busy():
		mixer.music.fadeout(1000)
		import time
#		mixer.music.stop()
	       
		
	
