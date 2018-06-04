import pygame
import matplotlib 
import trafficenv
import envstate
import time
import random
import agent
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import envstate
import os
import random
import math

x = 400
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)


plt.ion()
plt.show()

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Traffic Simulator")

traffic_env = trafficenv.TrafficEnv(hz = 200, sim_speed = 20)

spawn_rate = 60
	
i = 0
j = 0

#time between actions taken
action_time = 8
actions_per_episode = 10

total_episodes = 9

training_frequency = 3

total_reward = 0

gamma = 0.99

training_iterations = 0
tf.reset_default_graph() #Clear the Tensorflow graph.

myAgent = agent.Agent(lr=1.2e-2, s_size=5 ,a_size=2, h_size=25) #Load the agent.

init = tf.global_variables_initializer()
saver = tf.train.Saver()
f0 = open('data.txt', 'w')
f1 = open('wait.txt', 'w')

with tf.Session() as sess:
	saver.restore(sess, 'C:\\Users\\Ryan\\School\\EE\\EE509\\project\\agent.ckpt')
	sess.run(init)

	rewards = []
	trains = []
	avg_wait_time = 0
	#total_length = []
        
	expected_num_cars = 0
	total_num_cars = 0

	first_action = True

	gradBuffer = sess.run(tf.trainable_variables())
	for ix,grad in enumerate(gradBuffer):
		gradBuffer[ix] = grad * 0

	num_points = 0
	while num_points < 10:
		while i < total_episodes and envstate.running:
			print('episode: ' + str(i))

			s = traffic_env.reset()

			ep_history = []
			d = False

			mid = random.random() 
			r0 = random.random()*(0.05 + num_points/20) #random.uniform(0, mid)  #trained at 0.2
			r1 = random.random()*(0.05 + num_points/20) #mid - r0

			r2 = random.random()*(0.05 + num_points/20) ##random.uniform(0, 1 - mid) 
			r3 = random.random()*(0.05 + num_points/20) #1 - mid - r2

			rate = random.randint(1, 60) / 60

			#0 - west east
			#1 - north south
			state = 0
			while j < actions_per_episode and d == False and envstate.running:
				a_dist = sess.run(myAgent.output, feed_dict = {myAgent.state_in : [s]})
	            
				a = np.random.choice(a_dist[0], p = a_dist[0])
				a = np.argmax(a_dist == a)
				
				print('performing action: ' + str(a) + ', ' + str(j))
				(s1, r, d) = traffic_env.step(a, action_time, screen, rate, r0, r1, r2, r3, first_action)
				
				ep_history.append([s,a,r,s1])

				if first_action:
					first_action = False

				#print state
				#print('state: ' + str(s1[0]))
				#print('N: ' + str(s1[1]))
				#print('E: ' + str(s1[2]))
				#print('S: ' + str(s1[3]))
				#print('W: ' + str(s1[4]))
				#print('reward: ' + str(r))
				
				s = s1
				#plot average total reward of each episode vs policy
				total_reward += r

				j += 1   

				avg_wait_time += envstate.total_wait_time

	#		expected_num_cars += spawn_rate
			total_num_cars += envstate.total_num_cars
			print(str(total_num_cars) + ' ' + str(envstate.total_num_cars))
	#		print("spawn_rate: " + str(expected_num_cars) + " " + str(total_num_cars))

			first_action = True

			i += 1
			j = 0

			ep_history = np.array(ep_history)
			ep_history[:,2] = agent.discount_rewards(ep_history[:,2], gamma)
	        
	        #passes history of all rewards, all actions, all states
			feed_dict = {myAgent.reward_holder : ep_history[:,2], \
					     myAgent.action_holder : ep_history[:,1], \
						 myAgent.state_in      : np.vstack(ep_history[:,0])}                

			grads = sess.run(myAgent.gradients, feed_dict=feed_dict)
	        
			for idx,grad in enumerate(grads):
				gradBuffer[idx] += grad

			if i % training_frequency == 0:
				print('\nTraining Network\n')

				feed_dict = dict(zip(myAgent.gradient_holders, gradBuffer))
				for ix,grad in enumerate(gradBuffer):
					gradBuffer[ix] /= training_frequency
	           
				sess.run(myAgent.update_batch, feed_dict=feed_dict)

				for ix,grad in enumerate(gradBuffer):
					gradBuffer[ix] = grad * 0

				
		#		rewards.append(total_reward / training_frequency)

		#		trains.append(training_iterations)
		#		plt.plot(trains, rewards)
		#		plt.draw()
		#		plt.pause(0.001)
					
		#		training_iterations += 1

				
		f0.write(str(total_num_cars/total_episodes) + ' ' + str(total_reward / total_episodes) + '\n\r')
		f1.write(str(total_num_cars/total_episodes) + ' ' + str((avg_wait_time/total_num_cars) / total_episodes) + '\n\r')
		
		total_reward = 0
		avg_wait_time = 0
		num_points += 1
		total_num_cars = 0
		i = 0
		print('\n\n\n increasing traffic flow!!!\n\n\n')
#	plt.show()
	saver.save(sess, 'C:\\Users\\Ryan\\School\\EE\\EE509\\project\\agent.ckpt')

f0.close()	 
f1.close()	 
