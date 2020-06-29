from utils import *
from matplotlib.patches import RegularPolygon
import matplotlib.pyplot as plt
import streamlit as st 
import math

# rendering helper method
def convert(x,y):
	xmult = -1 -math.sin(math.radians(30))
	yadd = 2*math.cos(math.radians(30))
	if x % 2 == 0:
		return (x*xmult, y*yadd)
	else:
		return (x*xmult,  (y-.5)*yadd)

# main drawing function for board
def plotBoard(board, res, nums):
	m,n = res.shape
	fig, ax = plt.subplots(1)
	ax.set_aspect('equal')

	for x in range(m):
		for y in range(n):
			if all([board[i,j] == 0 for i,j in getNeighbors(board,x,y)]):
				continue
			color = colors[res[x,y]]# matplotlib understands lower case words for colours
			j,i = convert(x,y)
			hex = RegularPolygon((i,j), numVertices=6, radius=1, facecolor=color, alpha=0.4, edgecolor='black', linestyle='-')
			ax.add_patch(hex)
			# ax.text(i, j+0.2, f'{x},{y}', ha='center', va='center', size=10)
			if nums[x,y] != 0:
				if nums[x,y] == 6 or nums[x,y] == 8:
					ax.text(i, j, f'{nums[x,y]}', ha='center', va='center', size=10, color='red')
				else:
					ax.text(i, j, f'{nums[x,y]}', ha='center', va='center', size=10)

	ax.axis('off')
	mx, my = convert(0,0)
	tx, ty = convert(m-1, n-1)
	plt.ylim(tx-2, mx+2)
	plt.xlim(my-2, ty+2)
	st.pyplot()

