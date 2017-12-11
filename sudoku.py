import copy
su = [range(1,10) for i in range(9)]
row = [range(1,10) for i in range(9)]
col = [range(1,10) for i in range(9)]


#easy
doku = [[0,0,9,0,0,7,0,0,0],[3,6,0,0,4,0,5,8,0],
		[0,0,1,5,6,2,9,0,0],[0,3,8,0,0,6,0,0,0],
		[0,7,0,3,2,9,0,1,0],[0,0,0,1,0,0,3,6,0],
		[0,0,2,7,8,5,4,0,0],[0,8,4,0,1,0,0,2,9],
		[0,0,0,2,0,0,6,0,0]]

#easy
doku = [[6,0,7,8,0,9,0,2,5],[9,0,3,4,5,6,0,0,0],
		[0,4,0,0,0,0,6,0,0],[1,0,0,0,0,0,0,8,0],
		[0,7,0,2,0,4,0,3,0],[0,5,0,0,0,0,0,0,1],
		[0,0,9,0,0,0,0,5,0],[0,0,0,6,2,1,9,0,8],
		[2,8,0,7,0,5,3,0,6]]

#hard
#doku = [[2,0,0,0,7,0,0,0,0],[0,8,0,6,0,0,0,0,0],
#		[0,0,3,0,0,4,1,7,0],[0,0,0,8,6,5,0,0,1],
#        [3,0,0,0,2,0,0,0,9],[8,0,0,3,9,1,0,0,0],
#		[0,7,8,2,0,0,6,0,0],[0,0,0,0,0,6,0,4,0],
#		[0,0,0,0,1,0,0,0,3]]


#evil
doku = [[0,0,8,0,5,0,0,0,0],[6,0,0,0,0,0,0,0,2],
		[0,0,5,6,3,1,0,0,0],[3,0,0,0,0,0,0,8,0],
		[7,0,2,1,0,5,3,0,4],[0,4,0,0,0,0,0,0,1],
		[0,0,0,4,6,2,7,0,0],[8,0,0,0,0,0,0,0,5],
		[0,0,0,0,1,0,6,0,0]]

def recurSudoku(doku, flg = False):
	su = [range(1,10) for i in range(9)]
	row = [range(1,10) for i in range(9)]
	col = [range(1,10) for i in range(9)]
	for i in range(0,len(doku)):
		for j in range(0,len(doku)):
			try:
				row[i].remove(doku[i][j])
				col[j].remove(doku[i][j])
				su[(i//3)*3 + (j//3)].remove(doku[i][j])
			except ValueError:
				continue
	cnt = 0
	r = []
	while sum(map(lambda x: sum(x),doku)) != 405:
		cnt += 1
		if cnt>30 :
			return (doku, False)
		for i in range(0, len(doku)):
			for j in range(0, len(doku)):
				if doku[i][j] == 0:
					r = list(set(su[(i//3)*3 + (j//3)]).intersection(col[j]).intersection(row[i]))
					if len(r) == 1:
						print r[0], ' at ',i, j
						doku[i][j] = r[0]
						row[i].remove(doku[i][j])
						col[j].remove(doku[i][j])
						su[(i//3)*3 + (j//3)].remove(doku[i][j])
					elif len(r) == 2 and cnt>10:
						for k in r:
							print "trying ",k, ' at ',i, j
							doku[i][j] = k
							(d,f) = recurSudoku(copy.deepcopy(doku))
							if f:
								doku = d
								return(doku,True)
						return (doku,False)
					elif len(r) > 2 and cnt>20:
						for k in r:
							print "trying ",k, ' at ',i, j
							doku[i][j] = k
							(d,f) = recurSudoku(copy.deepcopy(doku))
							if f:
								doku = d
								return(doku,True)
						return(doku,False)
	print "count:", cnt
	return (doku,True)


def printSudoku(doku):
	for i in doku:
		st = ''
		for j in i:
			st = st + str(j) + '  '
		print st

if __name__ == "__main__":
	print "Solving Sudoku:"
	printSudoku(doku)
	(d,f) = recurSudoku(doku)
	if f:
		print "Routine Completed, Solved Sudoku:"
		printSudoku(d)
	else:
		print "Failed"
		printSudoku(d)
