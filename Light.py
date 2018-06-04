import Controller
import pygame
import World



class TrafficLight:
	initial_state = 'RED'
	state = 'RED'
	last_state = 'GREEN'
	bounding_box = []
	color = (255, 255, 50)

	direction = 'NORTH'

	#road bounds is 110 wide 195 long

	HEIGHT = 155
	WIDTH = 195

	def __init__(self, state, direction):
		self.direction = direction
		self.state = state
		self.initial_state = state
		if direction == World.EAST:
			self.WIDTH = 195
			self.HEIGHT = 55
			self.bounding_box = pygame.Rect(350, 450, self.WIDTH, self.HEIGHT)
		if direction == World.SOUTH:
			self.WIDTH = 55
			self.HEIGHT = 195
			self.bounding_box = pygame.Rect(545, 200, self.WIDTH, self.HEIGHT)
		if direction == World.NORTH:
			self.WIDTH = 55
			self.HEIGHT = 195
			self.bounding_box = pygame.Rect(600, 505, self.WIDTH, self.HEIGHT)
		if direction == World.WEST:
			self.WIDTH = 195
			self.HEIGHT = 55
			self.bounding_box = pygame.Rect(655, 395, self.WIDTH, self.HEIGHT)

	def update(self, dt):
		if self.state == 'YELLOW' and self.last_time != None and pygame.time.get_ticks() - self.last_time > yellow_time:
			self.last_time = None
			self.state = 'RED'

	def set_state(state):
		self.state = state;

	def render(self, screen):
		if self.state == 'RED':
			color = (255, 40, 40)
		if self.state == 'GREEN':
			color = (20, 255, 40)
		elif self.state == 'YELLOW':
			color = (255, 255, 50)
		pygame.draw.rect(screen, color, self.bounding_box, 0)

	def reset(self):
		self.state = self.initial_state
