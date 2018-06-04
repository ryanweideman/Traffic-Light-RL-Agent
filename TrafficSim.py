from Utility import *
import World
import pygame
import Controller
import matplotlib 
import envstate as env
		
class TrafficEnv:
	def __init__(self, hz = 200, sim_speed = 5, spawn_rate = 60):
		self.intersection_state = 0

		self.state = np.array((self.intersection_state, \
							   env.northward_cars_waiting, \
							   env.eastward_cars_waiting, \
							   env.southward_cars_waiting, \
							   env.westward_cars_waiting))

		self.reward = 0
		self.done = False

		self.intersection = World.Intersection()
		self.traffic_control = Controller.TrafficController()

		self.img = pygame.image.load("intersection.png").convert()

	def step(action, action_time, screen):
		#take the action here

		step_start_time = pygame.time.get_ticks()
		dt_start_time = step_start_time
		sim_one_sec_timer = step_start_time

		while (pygame.time.get_ticks() - step_start_time) < (action_time / self.sim_speed):
			#handle events, keypresses
			handle_input()

			if pygame.time.get_ticks() - dt_start_time > 1000/self.hz:
				dt = ((current_time - start_time) / 1000) * self.sim_speed				
				
				traffic_control.update(dt)
				intersection.update(dt)
				
				render(screen)

				dt_start_time = pygame.time.get_ticks()

			if pygame.time.get_ticks() - sim_one_sec_timer > (1000 / self.sim_speed):
				sim_one_sec_timer = pygame.time.get_ticks()
				intersection.spawn_cars(self.spawn_rate)	

		self.state = np.array((self.intersection_state, \
			   				env.northward_cars_waiting, \
			   				env.eastward_cars_waiting, \
			   				env.southward_cars_waiting, \
			   				env.westward_cars_waiting))
		#
		#calculate reward here
		#

		return self.state, self.reward, self.done

	def reset(self):
		intersection.reset()
		traffic_control.reset()


	def render(screen):
		screen.blit(self.img, (0, 0))

		intersection.render(screen)

		total_run_time = font.render('run_time: ' + str(pygame.time.get_ticks() // 1000), False, (255, 255, 255))
		screen.blit(total_run_time,(50,20))

		sim_time = (int)(pygame.time.get_ticks() // (1000 / simulation_speed))
		sim_run_time = font.render('sim_time: ' + str(int(sim_time)), False, (255, 255, 255))
		screen.blit(sim_run_time,(50,50))

		#wait times
		total_wait_time = font.render('total_wait_time: ' + str(int(World.total_wait_time)), False, (255, 255, 255))
		screen.blit(total_wait_time,(50,140))

		if World.num_cars_passed != 0:
			avg_wait_time = font.render('avg_wait_time: ' + '{0:0.2f}'.format(World.total_wait_time / World.num_cars_passed), False, (255, 255, 255))
			screen.blit(avg_wait_time,(50,170))

		#car counts
		north_car_count = font.render('north_cars_wait: ' + str(int(World.southward_cars_wait_time)), False, (255, 255, 255))
		screen.blit(north_car_count,(50,210))
		east_car_count = font.render('east_cars_wait:  ' + str(int(World.westward_cars_wait_time)), False, (255, 255, 255))
		screen.blit(east_car_count,(50,240))
		south_car_count = font.render('south_cars_wait: ' + str(int(World.northward_cars_wait_time)), False, (255, 255, 255))
		screen.blit(south_car_count,(50,270))
		west_car_count = font.render('west_cars_wait:  ' + str(int(World.eastward_cars_wait_time)), False, (255, 255, 255))
		screen.blit(west_car_count,(50,300))


		total_car_count = font.render('total_cars_passed: ' + str(World.num_cars_passed), False, (255, 255, 255))
		screen.blit(total_car_count,(50,340))

		life_wasted = font.render('minutes_of_life_wasted: ' + str(int(World.total_wait_time / 60)), False, (255, 255, 255))
		screen.blit(life_wasted,(750,20))

		current_action = font.render('current_action: ' + str(action_count), False, (255, 255, 255))
		screen.blit(current_action,(50,680))
		current_episode = font.render('current_episode: ' + str(episode_count), False, (255, 255, 255))
		screen.blit(current_episode,(50,710))
		epoch = font.render('current_epoch: ' + str(epoch_count), False, (255, 255, 255))
		screen.blit(epoch,(50,740))

		pygame.display.update()

if __name__ == '__main__':
	main()