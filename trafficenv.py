from Utility import *
import World
import pygame
import Controller
import matplotlib 
import envstate as env
import numpy as np

def handle_input():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			env.running = False

class TrafficEnv:
	def __init__(self, hz = 200, sim_speed = 1):
		self.intersection_state = 0
		self.hz = hz
		self.sim_speed = sim_speed

		self.state = np.array((self.intersection_state, \
			   				env.north_cars_wait_time, \
			   				env.east_cars_wait_time, \
			   				env.south_cars_wait_time, \
			   				env.west_cars_wait_time))
		
		self.reward = 0
		self.done = False
		self.prev_total_wait_time = 0

		self.intersection = World.Intersection()
		self.traffic_control = Controller.TrafficController()

		self.img = pygame.image.load("intersection.png").convert()
		self.time = 0


	def step(self, action, action_time, screen, rate, r0, r1, r2, r3, first):
	
		#toggles light if action is not the same as the current state
		if action != self.intersection_state:
			self.traffic_control.toggle_lights()
			self.intersection_state = action

		step_start_time = pygame.time.get_ticks()
		dt_start_time = step_start_time
		sim_one_sec_timer = step_start_time

		env.total_wait_time = 0

		#forward simulate action_time simulation seconds
		#breaks from loop if episode is determined to be ended
		while (pygame.time.get_ticks() - step_start_time) / 1000 < (action_time / self.sim_speed):
			handle_input()

			current_time = pygame.time.get_ticks()

			if current_time - dt_start_time > 1000/self.hz:
				dt = ((current_time - dt_start_time) / 1000) * self.sim_speed				
				self.time += dt

				self.traffic_control.update(dt, self.sim_speed)
				self.intersection.update(dt)
				
				self.render(screen)

				dt_start_time = current_time

			if pygame.time.get_ticks() - sim_one_sec_timer > (1000 / self.sim_speed):
				sim_one_sec_timer = pygame.time.get_ticks()
				self.intersection.spawn_cars(rate, r0, r1, r2, r3)

		self.state = np.array((self.intersection_state, \
			   				env.north_cars_wait_time, \
			   				env.east_cars_wait_time, \
			   				env.south_cars_wait_time, \
			   				env.west_cars_wait_time))
	
		if first:
			self.reward = 0
		else:
			self.reward = self.prev_total_wait_time - env.total_wait_time	

		self.prev_total_wait_time = env.total_wait_time

		return self.state, self.reward, self.done

	def reset(self):
		retstate = self.state

		self.intersection.reset()
		self.traffic_control.reset()

		self.intersection_state = 0
		self.sim_time = 0

		env.north_cars_waiting = 0
		env.east_cars_waiting = 0
		env.south_cars_waiting = 0
		env.west_cars_waiting = 0

		env.total_wait_time = 0
		env.num_cars_passed = 0
		env.total_num_cars = 0

		self.prev_total_wait_time = 0

		return retstate

	def render(self, screen):

		font = pygame.font.SysFont('Courier New', 26)#'Comic Sans MS'
		screen.blit(self.img, (0, 0))

		self.intersection.render(screen)

		total_run_time = font.render('run_time: ' + str(pygame.time.get_ticks() // 1000), False, (255, 255, 255))
		screen.blit(total_run_time,(50,20))

		sim_time = (int)(self.time)
		sim_run_time = font.render('sim_time: ' + str(int(sim_time)), False, (255, 255, 255))
		screen.blit(sim_run_time,(50,50))

		#wait times
		total_wait_time = font.render('total_wait_time: ' + str(int(env.total_wait_time)), False, (255, 255, 255))
		screen.blit(total_wait_time,(50,140))

		if env.num_cars_passed != 0:
			avg_wait_time = font.render('avg_wait_time: ' + '{0:0.2f}'.format(env.total_wait_time / env.num_cars_passed), False, (255, 255, 255))
			screen.blit(avg_wait_time,(50,170))

		#car delays
		north_car_delay = font.render('north_cars_wait: ' + str(int(env.north_cars_wait_time)), False, (255, 255, 255))
		screen.blit(north_car_delay,(50,210))
		east_car_delay = font.render('east_cars_wait:  ' + str(int(env.east_cars_wait_time)), False, (255, 255, 255))
		screen.blit(east_car_delay,(50,240))
		south_car_delay = font.render('south_cars_wait: ' + str(int(env.south_cars_wait_time)), False, (255, 255, 255))
		screen.blit(south_car_delay,(50,270))
		west_car_delay = font.render('west_cars_wait:  ' + str(int(env.west_cars_wait_time)), False, (255, 255, 255))
		screen.blit(west_car_delay,(50,300))


		total_car_count = font.render('total_cars_passed: ' + str(env.num_cars_passed), False, (255, 255, 255))
		screen.blit(total_car_count,(50,340))

#		current_action = font.render('current_action: ' + str(action_count), False, (255, 255, 255))
#		screen.blit(current_action,(50,680))
#		current_episode = font.render('current_episode: ' + str(episode_count), False, (255, 255, 255))
#		screen.blit(current_episode,(50,710))

		pygame.display.update()

if __name__ == '__main__':
	main()