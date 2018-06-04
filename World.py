from Car import *
import Controller
import Light
import random
import numpy as np
import envstate as env

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

car_list = []
traffic_light_list = []

light_north = Light.TrafficLight("RED", NORTH)
light_east = Light.TrafficLight("GREEN", EAST)
light_south = Light.TrafficLight("RED", SOUTH)
light_west = Light.TrafficLight("GREEN",WEST)

class Intersection:
	center_x = 600
	center_y = 450

	WIDTH = 110

	def __init__(self):
		traffic_light_list.append(light_north)
		traffic_light_list.append(light_east)
		traffic_light_list.append(light_south)
		traffic_light_list.append(light_west)

	def update(self, dt):
		env.north_cars_wait_time = 0
		env.east_cars_wait_time = 0
		env.south_cars_wait_time = 0
		env.west_cars_wait_time = 0

		for car in car_list:
			car.update(self, dt);

			if car.direction == SOUTH:
				env.north_cars_wait_time += car.wait_time				
			if car.direction == WEST:
				env.east_cars_wait_time += car.wait_time
			if car.direction == NORTH:
				env.south_cars_wait_time += car.wait_time
			if car.direction == EAST:
				env.west_cars_wait_time += car.wait_time


	def spawn_cars(self, rate, r0, r1, r2, r3):
		if random.random() < r0:
			car_list.append(Car(575, -500, 0, SOUTH, 100, (92, 152, 249)));
			env.total_num_cars += 1
		if random.random() < r1:
			car_list.append(Car(1700, 425, 0, WEST, 100, (92, 152, 249)));
			env.total_num_cars += 1
		if random.random() < r2:
			car_list.append(Car(625, 1400, 0, NORTH, 100, (92, 152, 249)));
			env.total_num_cars += 1
		if random.random() < r3:
			car_list.append(Car(-500, 475, 0, EAST, 100, (92, 152, 249)));
			env.total_num_cars += 1


	def render(self, screen):		
		for light in traffic_light_list:
			light.render(screen)

		for car in car_list:
			car.render(screen)


	def get_traffic_light(self, direction):
		if direction == NORTH:
			return light_north
		if direction == EAST:
			return light_east
		if direction == SOUTH:
			return light_south
		if direction == WEST:
			return light_west

	def reset(self):
		light_north.reset()
		light_east.reset()
		light_south.reset()
		light_west.reset()

		car_list[:] = []


