
import streamlit as st 
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
# import numpy as np
# import pandas as pd
# from collections import Counter
import random
import plotly.graph_objects as go
# from boards.classic import Classic
# from boards.classic56 import Classic56
# from features import *
# from utils import *
# from drawing import plotBoard


@st.cache(allow_output_mutation=True)
def getDice(_):
	return list(), [0 for i in range(13)]

def main():
	st.title('Catan Dice Tool')

	prev, stats = getDice(0)

	expected = [1,2,3,4,5,6,5,4,3,2,1]

	# buttons
	if st.button('Clear Dice'):
		while prev:
			prev.pop()
		for i in range(13):
			stats[i] = 0

	if st.button('Roll Dice'):
		da = random.randint(1,6)
		db = random.randint(1,6)

		st.markdown(f'## {da} + {db} = {da+db}')
		prev.append(da+db)
		stats[da+db] += 1

	# plot history
	if len(prev) > 4:
		for num in prev[-4::][::-1]:
			st.write(num)
	else:
		for num in prev[::-1]:
			st.write(num)

	# plot stats
	st.header('Dice Statistics')
	fig = go.Figure(data=[go.Bar(x=list(range(2,13)), y=stats[2:], name='# of rolls')], layout=go.Layout(barmode='overlay'))
	fig.add_trace(go.Bar(
    	x=list(range(2,13)), y=[sum(stats) *dots/36.0 for dots in expected] , opacity=.2, name='Expected Value'
	))
	fig.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        tick0 = 2,
        dtick = 1
    )
)
	st.plotly_chart(fig)


if __name__ == "__main__":
    main()