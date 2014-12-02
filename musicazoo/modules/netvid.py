import os
import tempfile
import threading
import time

import musicazoo.lib.vlc_player_compat as player
from musicazoo.lib.loading import LoadingScreen

class NetVid:
	TYPE_STRING='netvid'

	def __init__(self,queue,uid,url,short_description=None,long_description=None):
		self.player=player.Player()
		self.queue=queue
		self.uid=uid
		self.url=url
		self.duration=None
		self.time=None
		self.status='added'
		self.rate=None

		self.short_description=short_description
		if long_description is not None:
			self.long_description=long_description
		else:
			self.long_description=short_description

	def get_url(self):
		return self.url

	def get_duration(self):
		return self.duration

	def get_time(self):
		return self.time

	def get_status(self):
		return self.status

	def get_short_description(self):
		return self.short_description

	def get_long_description(self):
		return self.long_description

	def play(self):
		self.show_loading_screen()
		if self.status=='invalid':
			return
		self.vidPlay()
		self.status='finishing'

	def show_loading_screen(self):
		self.loading_screen=LoadingScreen()
		self.loading_screen.show()

	def hide_loading_screen(self):
		self.loading_screen.close()

	def pause(self):
		if self.status == 'paused':
			return
		if self.status != 'playing':
			raise Exception("Video is not playing")
		self.player.pause()
		self.status='paused'

	def stop(self):
		if self.status == 'stopped':
			return
		if not self.player.up():
			raise Exception("Video is not up")
		self.player.stop()

		if self.status=='loading':
			self.hide_loading_screen()

		self.status='stopped'

	def resume(self):
		if self.status == 'playing':
			return
		if self.status != 'paused':
			raise Exception("Video is not paused")
		self.player.play()
		self.status='playing'

	def vidPlay(self):
		self.player.load(self.url)

		self.status='loading'

		# Loop continuously, getting output and setting titles
		while self.player.up():
			time.sleep(0.1)
			t=self.player.time()
			if t is not None:
				if self.status=='loading':
					self.hide_loading_screen()
					self.status='playing'
				self.time=t
				self.duration=self.player.length()
				self.rate=self.player.get_rate()

		if self.status=='loading':
			self.hide_loading_screen()

		self.rate=None
		self.player.stop()

	def set_rate(self,rate):
		if not self.player.up():
			raise Exception("Cannot set rate of video that is not playing")
		self.player.set_rate(rate)

	def get_rate(self):
		return self.rate

	def seek_rel(self,offset):
		if not self.player.up():
			raise Exception("Video is not up")
		self.player.seek_rel(offset)

	def seek_abs(self,position):
		if not self.player.up():
			raise Exception("Video is not up")
		self.player.seek_abs(position)

	# Class variables

	commands={
		'pause':pause,
		'resume':resume,
		'stop':stop,
		'set_rate':set_rate,
		'seek_rel':seek_rel,
		'seek_abs':seek_abs,
	}

	parameters={
		'url':get_url,
		'duration':get_duration,
		'status':get_status,
		'time':get_time,
		'rate':get_rate,
		'short_description':get_short_description,
		'long_description':get_long_description,
	}

