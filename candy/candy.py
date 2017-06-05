# 10x10 2-dimention array
# 5 number to represent 5 kind of color
# Input two coordinate each round
#  1. can exchange if is adjacent
#  2. at least 3 same color in line can exchage
#     and elminate the object.
#  3. 1 elimination get 1 point.
# Total 20 round, than print the grade.
import random as r
import re
import sys

class Candy:
	def __init__(self,*args):
		print("Start Candy Crush")
		self.round_num = 0
		self.grade = 0
		self.game = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
		if len(args)>0:
			self.color= args[0]
		else:
			self.color=5
		self.WaitInput()

	def WaitInput(self):
		while self.round_num < 20:
			self.CreatePuzzle()
			print("Round:"+str(self.round_num))
			print("Grade:"+str(self.grade))
			action = raw_input("Input:")
			b = re.findall(r'\d', action)
			while not self.Is_vailed(b):
				action = raw_input()
				b = re.findall(r'\d', action)
			self.round_num+=1
		print("=====Game over=====")
		print("   Total Grade:" + str(self.grade))
		print("===================")

	def clear(self, mini=0, maxi=9):
		x=y=mini
		elim = []
		while x < maxi :
			while y < maxi:
				num = self.lookup(x,y)
				if num >= 2:
					for i in range(num+1):
						if elim.count((x,y+i))==0:
							elim.append((x, y+i))
					y+=num+1
				else:
					y+=1
			y=mini
			x+=1

		x=y=mini
		while y < maxi:
			while x < maxi:
				num = self.lookright(x,y)
				if num >= 2:
					for i in range(num+1):
						if elim.count((x+i,y))==0:
							elim.append((x+i,y))
					x+=num+1
				else:
					x+=1
			x=mini
			y+=1

		if len(elim) == 0:
			if not self.checkpos():
				self.game = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
				self.CreatePuzzle()
		else:
			print("cleaning..")
			self.grade += len(elim)
			elim.sort()
			while len(elim) > 0:
				tmp = elim.pop()
				out = self.game[tmp[0]].pop(tmp[1])
			print("Grade:"+str(self.grade))
			self.CreatePuzzle()

	def checkpos(self):
		for x in range(1,8):
			for y in range(1,8):
				if y < 6:
					if self.lookup(x,y) == 1:
						if self.game[x][y] == self.game[x][y+3]:
							return True
				if y > 2 :
					if self.lookdown(x,y) == 1:
						if self.game[x][y] == self.game[x][y-3]:
							return True
				if x < 6:
					if self.lookright(x,y) == 1:
						if self.game[x][y] == self.game[x+3][y]:
							return True
				if x > 2:
					if self.lookleft(x,y) == 1:
						if self.game[x][y] == self.game[x-3][y]:
							return True
				if y < 7:
					if self.game[x][y] == self.game[x][y+2]:
						if self.game[x][y] == self.game[x+1][y+1]:
							return True
						if self.game[x][y] == self.game[x-1][y+1]:
							return True
				if y > 1:
					if self.game[x][y] == self.game[x][y-2]:
						if self.game[x][y] == self.game[x+1][y-1]:
							return True
						if self.game[x][y] == self.game[x-1][y-1]:
							return True
				if x < 7:
					if self.game[x][y] == self.game[x+2][y]:
						if self.game[x][y] == self.game[x+1][y+1]:
							return True
						if self.game[x][y] == self.game[x+1][y-1]:
							return True
				if x > 1:
					if self.game[x][y] == self.game[x-2][y]:
						if self.game[x][y] == self.game[x-1][y+1]:
							return True
						if self.game[x][y] == self.game[x-1][y-1]:
							return True


		for i in [0,8]:
			for j in range(8):
				if self.game[i][j] == self.game[i][j+1]:
					if j > 2:
						if self.game[i][j] == self.game[i][j-3]:
							return True
					if j < 6:
						if self.game[i][j] == self.game[i][j+3]:
							return True
				if self.game[j][i] == self.game[j+1][i]:
					if j > 2:
						if self.game[j][i] == self.game[j-3][i]:
							return True
					if j < 6:
						if self.game[j][i] == self.game[j+3][i]:
							return True

		print("No possible match, refresh game.")
		return False

	def elimi(self, x1, y1, x2, y2):
		self.exchange([x1, y1, x2, y2])
		elim = []
		up = self.lookup(x1, y1)
		down = self.lookdown(x1, y1)
		if up+down >= 2:
			for i in range(up+down+1):
				if elim.count((x1,y1-down+i))==0:
					elim.append((x1, y1-down+i))
		left = self.lookleft(x1, y1)
		right = self.lookright(x1, y1)
		if left+right >= 2:
			for i in range(left+right+1):
				if elim.count((x1-left+i, y1))==0:
					elim.append((x1-left+i, y1))
		up = self.lookup(x2, y2)
		down = self.lookdown(x2, y2)
		if up+down >= 2:
			for i in range(up+down+1):
				if elim.count((x2,y2-down+i))==0:
					elim.append((x2, y2-down+i))
		left = self.lookleft(x2, y2)
		right = self.lookright(x2, y2)
		if left+right >= 2:
			for i in range(left+right+1):
				if elim.count((x2-left+i, y2))==0:
					elim.append((x2-left+i, y2))
		if len(elim) >0:
			self.grade+=len(elim)
			elim.sort()
			while len(elim) > 0:
				tmp = elim.pop()
				out = self.game[tmp[0]].pop(tmp[1])
			return False
		else:
			self.exchange([x1, y1, x2, y2])
			return True


	def Is_vailed(self, cor):
		if len(cor) == 4:
			for i in range(4):
				cor[i]=int(cor[i])
				if 1 > cor[i] or cor[i] > 9:
					print("Invailed input, type again:"),
					return False

			if (cor[0] != cor[2] and cor[1] != cor[3]):
				print("Not neighbor, type again:"),
				return False
			if cor[0] == cor[2]:
				if (cor[1]-cor[3])*(cor[1]-cor[3]) != 1:
					print("Not neighbor, type again:"),
					return False

			if cor[1] == cor[3]:
				if (cor[0]-cor[2])*(cor[0]-cor[2]) != 1:
					print("Not neighbor, type again:"),
					return False

			if  self.elimi(cor[0]-1, cor[1]-1, cor[2]-1, cor[3]-1):
				print("No possible match, type again:"),
				return False

			return True

		else:
			print("Invailed input, type again:"),
			return False

	def	lookup(self, x, y):
		if y < 8:
			if self.game[x][y] == self.game[x][y+1]:
				return self.lookup(x, y+1)+1
			else:
				return 0
		else:
			return 0
	def lookdown(self, x, y):
		if y > 0:
			if self.game[x][y] == self.game[x][y-1]:
				return self.lookdown(x, y-1)+1
			else:
				return 0
		else:
			return 0
	def lookright(self, x, y):
		if x < 8:
			if self.game[x][y] == self.game[x+1][y]:
				return self.lookright(x+1,y) + 1
			else:
				return 0
		else:
			return 0
	def lookleft(self, x, y):
		if x > 0:
			if self.game[x][y] == self.game[x-1][y]:
				return self.lookleft(x-1,y)+1
			else:
				return 0
		else:
			return 0



	def exchange(self, cor):
		self.game[cor[0]][cor[1]] += self.game[cor[2]][cor[3]]
		self.game[cor[2]][cor[3]] = self.game[cor[0]][cor[1]] - self.game[cor[2]][cor[3]]
		self.game[cor[0]][cor[1]] -= self.game[cor[2]][cor[3]]

	def CreatePuzzle(self):
		for i in range(9):
			while len(self.game[i]) < 9 :
				self.game[i].append(r.randint(1,self.color))
		self.PrintGame()
		self.clear()

	#Print the Game template.
	def PrintGame(self):
		for i in range(10):
			if i != 9:
				print("\033[1;31;40m" + str(9-i) + " " + "\033[0m"),
				for j in range(9):
					print(str(self.game[j][8-i]) + " "),
				print("")
			else:
				print("\033[1;31;40m"+"0  1  2  3  4  5  6  7  8  9"+"\033[0m")

if len(sys.argv) > 1:
	a = Candy(int(sys.argv[1]))
else:
	a = Candy()


