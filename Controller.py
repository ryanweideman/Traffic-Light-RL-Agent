from Car import *
import pygame
import World
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

class TrafficController:

	def __init__(self):
		self.light_timer_start = pygame.time.get_ticks()
		self.yellow_light_timer_start = pygame.time.get_ticks()
		self.light_timer = 0
		self.yellow_light_timer = 0
		self.toggle = False
		self.yellow_time = 2500

	def update(self, dt, sim_speed):
		if self.toggle and (pygame.time.get_ticks() - self.yellow_light_timer_start)  * sim_speed > self.yellow_time:
			self.toggle = False

			if World.light_east.state == 'YELLOW':
				World.light_east.state = 'RED'
				World.light_west.state = 'RED'
				World.light_south.state = 'GREEN'
				World.light_north.state = 'GREEN'

			if World.light_south.state == 'YELLOW':
				World.light_south.state = 'RED'
				World.light_north.state = 'RED'
				World.light_east.state = 'GREEN'
				World.light_west.state = 'GREEN'


	def toggle_lights(self):
		if World.light_east.state == 'GREEN':
			World.light_west.state = 'YELLOW'
			World.light_east.state = 'YELLOW'
		
		elif World.light_south.state == 'GREEN':
			World.light_south.state = 'YELLOW'
			World.light_north.state = 'YELLOW'

		self.toggle = True
		self.yellow_light_timer_start = pygame.time.get_ticks()

	def reset(self):
		self.toggle = False
