
from boards.classic import Classic

board = Classic()
res = board.genRes(maxClump=1)
nums = board.genNums(res, [0,0], [0,0], spread68=True, spread212=True, spreadNums=False)
