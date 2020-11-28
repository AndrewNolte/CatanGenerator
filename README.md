# Catan Board Generator [![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/andrewnolte/catangenerator/master/catan.py/+/)

## catan.py

* This is the main UI and logic flow

## catancsp.py

* This is the CSP solver that solves a board given contraints
* It provides a class for boards to extend from, as some may override the generation logic

## features.py

* This contains feature evaluators that take a board as input

## drawing.py

* This contains drawing functions, mainly for the board

## utils.py

* This contains utility functions for interacting with catan boards, as well as global constants/enums

## boards/

* This contains classes representing a version of a catan board with counts for pieces, board shape, etc.
* Each on extends a base class