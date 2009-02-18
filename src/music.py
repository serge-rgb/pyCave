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
	       
		
	
