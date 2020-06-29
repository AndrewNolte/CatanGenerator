

from heapq import heappush, heappop
import random
numToDot = [0,0,1,2,3,4,5,6,5,4,3,2,1]
# universal vars
tiles = ['ocean', 'desert', 'brick', 'wood', 'sheep', 'wheat', 'ore', 'gold']
colors = ['blue', 'tan', 'firebrick', 'darkgreen', 'lawngreen', 'gold', 'slategrey', 'darkkhaki']

# if at first you fail, try, try, try again
def iafyf(func):

	def wrapper(*args, **kwargs):
		res = None
		while res is None:
			try:
				res = func(*args, **kwargs)
			except:
				pass
		return res
	return wrapper

def getNeighbors(board, i,j):
	mt = (2*(i%2))-1
	for x,y in [  (i+1, j), (i-1, j),   (i+1, j-mt), (i-1, j-mt),   (i, j+1), (i, j-1) ]:
		if 0 <= x < board.shape[0] and 0 <= y < board.shape[1]:
			yield x,y

def getValidNeighbors(board, i,j):
	mt = (2*(i%2))-1
	for x,y in [  (i+1, j), (i-1, j),   (i+1, j-mt), (i-1, j-mt),   (i, j+1), (i, j-1) ]:
		if 0 <= x < board.shape[0] and 0 <= y < board.shape[1] and board[x,y] == 1:
			yield x,y


# dist is a counter
# constraints is a set of possible values to choose from
def sample(dist, possible=None):
	dst = dist.copy()
	if possible is not None:
		for i in dist:
			if i not in possible:
				dst[i] = 0
	opt = list(dst.elements())
	if len(opt) == 0:
		return None
	return random.choice(opt)

def cspLen(dist, possible):
	return sum([1 for i in dist if i in possible])

	
# a priority queue that assumes no duplicates, as the priorities can be updated via another push
class PQ:

	def __init__(self):
		self.heap = list()
		self.itemToPriority = dict()

	def push(self, item, priority):
		self.itemToPriority[item] = priority
		heappush(self.heap, (priority, item))
	
	def pop(self):
		while self.heap:
			priority, item = heappop(self.heap)
			# ignore items that dont match, they are old values
			if self.itemToPriority[item] == priority:
				# after returning with the correct priority, make sure the others are invalidated
				self.itemToPriority[item] = None
				return item, priority
	
	def getPriority(self, item):
		return self.itemToPriority.get(item)

	def hasStuff(self):
		for priority, item in self.heap:
			if self.itemToPriority[item] == priority:
				return True
		return False


	def iter(self):
		for pri, item in self.heap:
			yield item