import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np

class Agent():
    def __init__(self, lr, s_size,a_size,h_size):
        #These lines established the feed-forward part of the network. The agent takes a state and produces an action.
        
        #creates a placeholder tensor for the input.
        #s size is the number of inputs
        self.state_in = tf.placeholder(shape=[None,s_size],dtype=tf.float32)

        #https://www.tensorflow.org/api_docs/python/tf/contrib/layers/fully_connected
        #each call to fully connected adds a hidden layer to the network
        #h_size is the number neurons in the hidden layer, biases_initializer=None skips biases, activation_fn=tf.nn.relu ReLU is default but they set it anyways
        hidden = slim.fully_connected(self.state_in, h_size, biases_initializer=None, activation_fn=tf.nn.relu)
        
        #takes the output of the first part of the network and passes it to the output layer of the network, which uses the softmax activation fnct
        #a_size is the number of outputs. in the example, this is 2 because the cart moves left or right, for two actions
        self.output = slim.fully_connected(hidden, a_size, activation_fn=tf.nn.softmax, biases_initializer=None)

        #"Returns the index with the largest value across axes of a tensor", not sure what the 1 is
        self.chosen_action = tf.argmax(self.output,1)

        #The next six lines establish the training proceedure. We feed the reward and chosen action into the network
        #to compute the loss, and use it to update the network.
        self.reward_holder = tf.placeholder(dtype=tf.float32)
        self.action_holder = tf.placeholder(dtype=tf.int32)
        
        self.indexes = tf.range(0, tf.shape(self.output)[0]) * tf.shape(self.output)[1] + self.action_holder
        self.responsible_outputs = tf.gather(tf.reshape(self.output, [-1]), self.indexes)

        #REINFORCE algorithm
        self.loss = -tf.reduce_mean(tf.log(self.responsible_outputs)*self.reward_holder)
        
        #returns layers
        tvars = tf.trainable_variables()

        self.gradient_holders = []
        for idx,var in enumerate(tvars):
            placeholder = tf.placeholder(tf.float32,name=str(idx)+'_holder')
            self.gradient_holders.append(placeholder)
        
        #creates
        self.gradients = tf.gradients(self.loss, tvars)
        
        #Adam - adaptive learning rate
        optimizer = tf.train.AdamOptimizer(learning_rate=lr)
        
        #applyies gradients to variables
        self.update_batch = optimizer.apply_gradients(zip(self.gradient_holders, tvars))

def discount_rewards(r, gamma):
    #take 1D float array of rewards and compute discounted reward
    discounted_r = np.zeros_like(r)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r