from Utility import *
import Light
import World
import math
import pygame
import Controller
import envstate as env

class Car:
	bounding_box = None
	view_box = []
	angle = 0
	width = 0
	height = 0
	wait_time = 0
	max_wait_time = 0
	wait_time_start = None
	waiting = False
	LENGTH = 18*3
	WIDTH = 18

	past_intersection = False

	img = pygame.image.load("red_car.png")

	yellow_light_flag = 0

	#color is a tuple (r, g, b)
	def __init__(self, center_x, center_y, state, direction, speed, color):
		self.center_x = center_x
		self.center_y = center_y
		self.speed = speed
		self.color = color
		self.direction = direction

		width = 0
		height = 0

		if self.direction == World.EAST:
			self.width = self.LENGTH
			self.height = self.WIDTH
			self.angle = 0
			self.view_box = pygame.Rect(self.width, 0, 1.5*self.width, self.height)
		elif self.direction == World.WEST:
			self.width = self.LENGTH
			self.height = self.WIDTH
			self.angle = math.pi
			self.view_box = pygame.Rect(-self.width, 0, 1.5*self.width, self.height)
		elif self.direction == World.NORTH:
			self.width = self.WIDTH
			self.height = self.LENGTH
			self.angle = 3*math.pi/2
			self.view_box = pygame.Rect(0, -self.height, self.width, 1.5*self.height)
		elif self.direction == World.SOUTH:
			self.width = self.WIDTH
			self.height = self.LENGTH
			self.angle = math.pi/2
			self.view_box = pygame.Rect(0, self.height, self.width, 1.5*self.height)

		self.bounding_box = pygame.Rect(0, 0, self.width, self.height)
		self.update_bounding_box()

	def update(self, intersection, dt):
		ideal_speed = 130
		
		traffic_light = intersection.get_traffic_light(self.direction)

		#sets appropriate speed to react to traffic light
		if self.bounding_box.colliderect(traffic_light.bounding_box):
			if traffic_light.state == 'RED':
				distance = distance_btwn(self.center_x, self.center_y, intersection.center_x, intersection.center_y) - intersection.WIDTH/2 - 30
				ideal_speed = distance / 2 #this is an experimental constant
				self.yellow_light_flag = 0
			if traffic_light.state == 'YELLOW':
				distance = distance_btwn(self.center_x, self.center_y, intersection.center_x, intersection.center_y) - intersection.WIDTH/2 - 30
				
				#handles case where car is too deep into the yellow and must speed up to make it over the line
				if self.yellow_light_flag == 0:
					if distance < 3*195/4:
						ideal_speed = 160 #this is an experimental constant
						self.yellow_light_flag = 1
					else:
						ideal_speed = distance / 1.5 #this is an experimental constant
						self.yellow_light_flag = -1
				elif self.yellow_light_flag == 1:
					ideal_speed = 160
				elif self.yellow_light_flag == -1:
					ideal_speed = distance / 1.5

		closest_car_distance = -1
		for car in World.car_list:
			if car == self:
				continue
			if car.direction != self.direction:
				continue
			if self.view_box.colliderect(car.bounding_box):
				dist = distance_btwn(*self.bounding_box.center, *car.bounding_box.center) - 60#how far apart cars should be when they are stopped
				if closest_car_distance == -1:
					closest_car_distance = dist
				elif dist < closest_car_distance:
					closest_car_distance = dist
				
		if closest_car_distance != -1:
			ideal_speed = closest_car_distance / 2.5

		error = ideal_speed - self.speed
		
		#proportional controller
		self.speed += dt*error*3 #this is an experimental constant
	
		#integrate car's velocity
		self.center_x += self.speed * math.cos(self.angle) * dt;
		self.center_y += self.speed * math.sin(self.angle) * dt;


		self.update_bounding_box()

		#COLLECT METRICS HERE
		#
		#
		#

		#determines how long this particular car has been waiting, if its waiting
		if self.waiting == False and self.speed < 40:
			self.waiting = True
			if self.direction == World.EAST:
				env.west_cars_waiting += 1
			if self.direction == World.SOUTH:
				env.north_cars_waiting += 1
			if self.direction == World.WEST:
				env.east_cars_waiting += 1
			if self.direction == World.NORTH:
				env.south_cars_waiting += 1
		
		if self.waiting:
			env.total_wait_time += dt
			self.wait_time += dt
			self.max_wait_time = self.wait_time


		#handles end of wait time
		if self.direction == World.EAST and self.center_x > 655 and not self.past_intersection:
			env.num_cars_passed += 1
			if self.waiting:
				env.west_cars_waiting -= 1
				self.wait_time = 0
				self.waiting = False
			self.past_intersection = True
			
		if self.direction == World.SOUTH and self.center_y > 505 and not self.past_intersection:
			env.num_cars_passed += 1
			if self.waiting:
				env.north_cars_waiting -= 1
				self.wait_time = 0
				self.waiting = False
			self.past_intersection = True

		if self.direction == World.WEST and self.center_x < 545 and not self.past_intersection:
			env.num_cars_passed += 1
			if self.waiting:
				env.east_cars_waiting -= 1
				self.wait_time = 0
				self.waiting = False
			self.past_intersection = True

		if self.direction == World.NORTH and self.center_y < 395 and not self.past_intersection:
			env.num_cars_passed += 1
			if self.waiting:
				env.south_cars_waiting -= 1
				self.wait_time = 0
				self.waiting = False
			self.past_intersection = True


		#handles removing car
		self.handle_remove_car()

	def render(self, screen):		
		#uses corners to draw the car
		pygame.draw.rect(screen, self.color, self.bounding_box, 0)
		#pygame.draw.rect(screen, (2, 255, 255), self.view_box, 0)

	def update_bounding_box(self):
		cx = self.center_x
		cy = self.center_y
		width = self.width
		height= self.height

		self.bounding_box.center = (cx, cy)

		if self.direction == World.EAST:
			self.view_box.center = (cx+(0.5 + 0.75)*width, cy)
		elif self.direction == World.WEST:
			self.view_box.center = (cx-(0.5 + 0.75)*width, cy)
		elif self.direction == World.SOUTH:
			self.view_box.center = (cx, cy+(0.5 + 0.75)*height)
		elif self.direction == World.NORTH:
			self.view_box.center = (cx, cy-(0.5 + 0.75)*height)

	def handle_remove_car(self):
		if self.direction == World.EAST and self.center_x > 1250:
			World.car_list.remove(self)
		elif self.direction == World.SOUTH and self.center_y > 1000:
			World.car_list.remove(self)
		elif self.direction == World.WEST and self.center_x < -50:
			World.car_list.remove(self)
		elif self.direction == World.NORTH and self.center_y < -75:
			World.car_list.remove(self)




