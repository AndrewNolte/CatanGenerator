from utils import *

def getClumpiness(board):
	m,n = board.shape
	cnt = 0
	for i in range(m):
		for j in range(n):
			for x,y in getNeighbors(board, i, j):
				if board[x][y] == board[i][j] and board[x][y] >= 2:
					cnt += 1
	return cnt//2

# sum up the dots of production for each resource
def getProductions(res, nums):
	m,n = res.shape
	cnts = [0 for i in range(len(tiles))]
	for i in range(m):
		for j in range(n):
			cnts[res[i,j]] += numToDot[nums[i,j]]
	
	return cnts

# each tile 'owns' a spot on the top and bottom of its hex
# distribution of productions of each spot
def getPositionCounts(res, nums):
	m,n = res.shape
	cnts = [0 for i in range(20)]
	# counts the top and bottom of hex
	for i in range(m):
		for j in range(n):
			top = numToDot[nums[i,j]]
			bot = numToDot[nums[i,j]]
			for x,y in getNeighbors(nums,i,j):
				if x == i-1:
					top += numToDot[nums[x,y]]
				elif x == i+1:
					bot += numToDot[nums[x,y]]
				
			cnts[top] += 1
			cnts[bot] += 1	
	return cnts[1:]