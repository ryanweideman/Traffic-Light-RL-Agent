import math

def distance_btwn(cx1, cy1, cx2, cy2):
	return math.sqrt((cx1 - cx2)**2 + (cy1 - cy2)**2)

class Vector:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;