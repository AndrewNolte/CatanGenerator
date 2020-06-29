
import numpy as np
from heapq import heappush, heappop
from utils import *
import streamlit as st 
# from catan import plotBoard
# from drawing import plotBoard

class CatanBoard:

	# each subclass will use this are to set up the board, tile counts, and num counts
	# some may override generation functions. For example, seafarers will use the classic board to 
	# generate a portion, then
	# finish the rest later
	# board objects are stateless (only store config and generation methods)
	# state of generation is stored outside, and passed in where necessary
	def __init__(self):
		self.board = None
		self.resCounts = None
		self.numCounts = None
		pass


	####################################################

	#############  CSP Solution       ##################

	####################################################
	# a general method for generating a resource and num board given constraints
	@iafyf
	def genRes(self, maxClump= None, maxClumps= None):
		# board = np.copy(self.board)
		
		# return self.genResRandom()

		# generate based on total clumps
		if maxClump is not None:
			res = np.zeros(self.board.shape, dtype = np.uint8)
			m,n = self.board.shape

			#resources to sample from
			smp = self.resCounts.copy()
			# set of possibilities for each tile to carry
			pos = set([i for i in range(len(self.resCounts)) if self.resCounts[i] > 0])
			# matrix of possiblities
			constraints = [[pos.copy() for i in range(n)] for j in range(m)]
			# store neighbor counts for easy conflict resolution
			nbs = [[[0 for i in range(len(tiles))] for j in range(n)] for k in range(m)]
			# priority queue for extracting the most-constrained tile
			pq = PQ()
			# data for main constraint
			curClumps = 0

			# push everything onto priority queue
			for x in range(m):
				for y in range(n):
					if self.board[x,y] == 1:
						pq.push((x,y), len(constraints[x][y]))

			# get the tile with the least number of possibilites
			while pq.hasStuff():
				(x,y), constraintLen = pq.pop()
				if res[x,y] > 0:
					continue

				cr = sample(smp, constraints[x][y])
				# cr may be None if constraints didn't work out
				smp[cr] -= 1
				res[x,y] = cr

				# increase neighbor count
				for i,j in getValidNeighbors(self.board,x,y):
					nbs[i][j][cr] += 1
					if nbs[i][j][cr] > (maxClump-curClumps) and cr in constraints[i][j]:
						constraints[i][j].remove(cr)
						pq.push((i,j), len(constraints[i][j]))

				# remove tile if we don't have more of it
				if smp[cr] == 0:
					for i,j in pq.iter():
						if cr in constraints[i][j]:
							constraints[i][j].remove(cr)
							pq.push((i,j), len(constraints[i][j]))
				
				# increase clump count, rectify with constraints if increased
				clumpsMade = False
				for i,j in getValidNeighbors(self.board,x,y):
					if res[i,j] == cr:
						curClumps += 1
						clumpsMade = True

				if clumpsMade:
					for i,j in pq.iter():
						for r in constraints[i][j].copy():
							if nbs[i][j][r] > (maxClump-curClumps):
								constraints[i][j].remove(r)
								pq.push((i,j), len(constraints[i][j]))
					

			return res


		return self.genResRandom()

	@iafyf
	def genNums(self, res, marketProduce=None, spotProduce=None, spread68=True, spread212=True, spreadNums=False):
		nums = np.zeros(self.board.shape, dtype = np.uint8)
		m,n = self.board.shape

		#resources to sample from and subtract from
		smp = self.numCounts.copy()
		# set of possibilities for each tile to carry
		numSet = set([i for i in range(len(self.numCounts)) if self.numCounts[i] > 0])
		# matrix of possiblities
		constraints = [[numSet.copy() for i in range(n)] for j in range(m)]
		# priority queue for extracting the most-constrained tile
		pq = PQ()

		# push everything onto priority queue
		for x in range(m):
			for y in range(n):
				if self.board[x,y] == 1:
					pq.push((x,y), len(constraints[x][y]))

		# constraints inherently imposed by desert
		if spread212:
			di, dj = np.where(res == tiles.index('desert'))

			for dx, dy in zip(list(di), list(dj)):
				for i,j in getValidNeighbors(self.board, dx, dy):
					constraints[i][j].discard(2)
					constraints[i][j].discard(12)

		# get the tile with the least number of possibilites
		while pq.hasStuff():
			(x,y), constraintLen = pq.pop()
			if nums[x,y] > 0 or res[x,y] == 1:
				continue

			

			curnum = sample(smp, constraints[x][y])
			# cr may be None if constraints didn't work out
			smp[curnum] -= 1
			nums[x,y] = curnum

			if spread68 and curnum == 6 or curnum == 8:
				for i,j in getValidNeighbors(self.board, x, y):
					constraints[i][j].discard(6)
					constraints[i][j].discard(8)


			if spread212 and curnum == 2 or curnum == 12:
				for i,j in getValidNeighbors(self.board, x, y):
					constraints[i][j].discard(2)
					constraints[i][j].discard(12)
			
			if spreadNums:
				for i,j in getValidNeighbors(self.board, x, y):
					constraints[i][j].discard(curnum)
					constraints[i][j].discard(curnum)

			# remove tile if we don't have more of it
			if smp[curnum] == 0:
				for i,j in pq.iter():
					if curnum in constraints[i][j]:
						constraints[i][j].remove(curnum)
						pq.push((i,j), len(constraints[i][j]))
		return nums

	####################################################

	#############  Random Generation  ##################

	####################################################

	def genResRandom(self):
		res = np.zeros(self.board.shape, dtype = np.uint8)
		m,n = self.board.shape
		smp = self.resCounts.copy()
		# st.write(board.shape)
		for x in range(m):
			for y in range(n):
				if self.board[x,y] == 1:
					res[x,y] = sample(smp)
					smp[res[x,y]] -= 1 
		return res

	def genNumsRandom(self, res):
		nums = np.zeros(res.shape, dtype = np.uint8)
		m,n = self.board.shape
		smp = self.numCounts.copy()
		# st.write(board.shape)
		for x in range(m):
			for y in range(n):
				if res[x][y] > 1:
					nums[x,y] = sample(smp)
					smp[nums[x,y]] -= 1
		return nums

	# TODO: figure out port formats, display, then write random generator
	def genPorts(self):
		pass

	def verify(self):
		spots = np.sum(self.board)
		res = True

		if sum(list(self.resCounts.values())) != spots:
			print('res counts does\'t add to spots available')
			res = False
		if sum(list(self.numCounts.values())) != spots-self.resCounts[1]:
			print('num counts does\'t add to spots available')
			res = False
		if self.numCounts[0] or self.numCounts[1] or self.numCounts[7]:
			print('invalid nums detected')
			res = False

		return res