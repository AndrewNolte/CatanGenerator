

from catancsp import CatanBoard
import numpy as np
from collections import Counter

class Classic56(CatanBoard):

	def __init__(self):
		self.board = np.array([   [0,0,0,0,0,0,0,0,0],\
								 [0,0,0,1,1,1,0,0,0],\
								  [0,0,1,1,1,1,0,0,0],\
							     [0,0,1,1,1,1,1,0,0],\
								  [0,1,1,1,1,1,1,0,0],\
							     [0,0,1,1,1,1,1,0,0],\
								  [0,0,1,1,1,1,0,0,0],\
								 [0,0,0,1,1,1,0,0,0],\
							      [0,0,0,0,0,0,0,0,0] ])
		self.resCounts = Counter({i:j for i,j in enumerate([0, 2, 5, 6, 6, 6, 5, 0])})
		self.numCounts = Counter({i:j for i,j in enumerate([0,0,2,3,3,3,3,0,3,3,3,3,2])})