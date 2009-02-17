import pygame.mixer as mixer

mixer.init(44100,-16,6,3072)
mixer.music.set_volume(1.0)

muted = False

def mute ():
	if muted == False:
		mixer.music.set_volume(0.0)
		muted = True
	else:
		mixer.music.set_volume(1.0)
		muted = False
	
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
	       
		
	
