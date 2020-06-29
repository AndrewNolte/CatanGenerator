

from catancsp import CatanBoard
import numpy as np
from collections import Counter

class Classic(CatanBoard):

	def __init__(self):
		self.board = np.array([   [0,0,0,0,0,0,0],\
								[0,0,1,1,1,0,0],\
							     [0,1,1,1,1,0,0],\
								[0,1,1,1,1,1,0],\
							     [0,1,1,1,1,0,0],\
								[0,0,1,1,1,0,0],\
							     [0,0,0,0,0,0,0] ])
		self.resCounts = Counter({i:j for i,j in enumerate([0, 1, 3, 4, 4, 4, 3, 0])})
		self.numCounts = Counter({i:j for i,j in enumerate([0,0,1,2,2,2,2,0,2,2,2,2,1])})