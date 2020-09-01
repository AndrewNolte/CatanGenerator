import streamlit as st 
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from collections import Counter
import random
import plotly.graph_objects as go
from boards.classic import Classic
from boards.classic56 import Classic56
from features import *
from utils import *
from drawing import plotBoard
# import plotly.express as px
# clump = st.sidebar.slider('clumpiness',0,10)
# dicestack = list()





@st.cache(allow_output_mutation=True)
def getBoard(_):
	return {'res':None, 'nums':None}

def main():

	st.title('Catan Board Generator')
	#####################################
	############ Sidebar inputs
	#####################################

	st.sidebar.markdown('# Board Parameters')
	# to do with resources
	maxClumps = st.sidebar.slider('Max Clumps', 0, 16, 2)

	# to do with resources and numbers
	# TODO: add csp support for market and spot produce
	# minProduce, maxProduce = st.sidebar.slider('Market Produce', 7, 20, [9,15])
	# minSpot, maxSpot = st.sidebar.slider('Location Produce', 7, 20, [9,15])
	minProduce, maxProduce = None, None
	minSpot, maxSpot = None,None

	# to do with numbers only
	spread68 = st.sidebar.checkbox('Spread out 6,8', value=True)
	spread212 = st.sidebar.checkbox('Spread out 2, 12, desert', value=True)
	spreadNums = st.sidebar.checkbox('Spread out identical numbers', value=False)

	# TODO: add advanced options for market produce by resource, and clumps by resource
	boards = {'Classic' : Classic(),
			'5-6 Player' : Classic56()}
	
	boardName = st.sidebar.selectbox('Board Type', list(boards.keys()))
	board = boards[boardName]

	if not board.verify():
		st.error('Error in board verification')
		return



	#####################################
	############ Map gen
	#####################################


	if st.button('Generate Map'):

		bd = getBoard(0)
		bd['board'] = board
		bd['res'] = board.genRes(maxClump=maxClumps)
		bd['nums'] = board.genNums(bd['res'] , (minProduce, maxProduce), (minSpot, maxSpot), spread68, spread212, spreadNums)

	bd = getBoard(0)
	if bd['res'] is not None:
		res = bd['res']
		nums = bd['nums']
		plotBoard(bd['board'].board, res, nums)
			# display features
		st.header(f'Clumps: {getClumpiness(res)}') 

		prod = getProductions(res, nums)
		spotprod = getPositionCounts(res, nums)

		st.header('Board Productions')
		fig = go.Figure(data=[go.Bar(x=tiles[3:-1], y=prod[3:-1])])
		fig.update_layout(
    # xaxis = dict(
    #     tickangle = 90,
    #     title_text = "Month",
    #     title_font = {"size": 20},
    #     title_standoff = 25),
    yaxis = dict(
        title_text = "# of spots",
        title_standoff = 25))
		st.plotly_chart(fig) 

		
		st.header('Spot Productions')
		fig = go.Figure(data=[go.Bar(x=list(range(1,20)), y=spotprod)])

		fig.update_layout(
    xaxis = dict(
        title_text = "dot count",
        title_font = {"size": 20},
        title_standoff = 25),
    yaxis = dict(
        title_text = "# of spots with dot count",
        title_standoff = 25))
		st.plotly_chart(fig) 

	# st.markdown('[Feedback/Bugs](https://forms.gle/J9ZubAui3LFbaNN47)')

	# print out globals for debugging

	# if st.sidebar.checkbox('debug', value=True):
		# for var, data in vars().copy().items():
		# 	if str(var).lower() != 'builtins':
		# 		st.info(str(var) + ':' + str(data))


if __name__ == "__main__":
    main()