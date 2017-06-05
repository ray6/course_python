import threading
import time
import random as r
exitFlag = False
card = None
bonus = [50, 20, 0, 0]
win = 0
pockers = []

class myThread(threading.Thread):
	def __init__(self, name):
		threading.Thread.__init__(self)
		self.name = name
		self.point = 0
		self.finish = False
	def run(self):
		global card
		global win
		global t0
		while not (exitFlag or self.finish):
			Lock.acquire()
			if not card == None:
				if time.time()-t0 > 1.5:
					self.point += 5
					pockers.pop(card)
					print("["+str(self.name)+"]:Rob!(5pt)")
					card = None
				else:
					for i in range(len(player[self.name])):
						if pockers[card][1] == player[self.name][i][1]:
							self.point += 30
							print("["+str(self.name)+"]:Fit "+ str(player[self.name][i])+"(30pt)")
							player[self.name].pop(i)
							pockers.pop(card)
							card = None
							if len(player[self.name]) == 0:
								self.point += bonus[win]
								win += 1
								print("["+str(self.name)+"]: finish!! Get "+ str(self.point) + " point.")
								self.finish = True
								break
							else:
								break
						elif pockers[card][0] == player[self.name][i][0]:
							self.point += 10
							print("["+str(self.name)+"]:Fit "+ str(player[self.name][i])+"(10pt)")
							player[self.name].pop(i)
							pockers.pop(card)
							card = None
							if len(player[self.name]) == 0:
								self.point += bonus[win]
								win += 1
								print("["+str(self.name)+"]: finish!! Get "+ str(self.point) + " point.")
								self.finish = True
								break
							else:
								break
			Lock.release()





def pocker():
	for i in range(1,5):
		for j in range(1, 14):
			pockers.append((i, j))

def giveCard():
	for i in range(3):
		for j in player:
			if len(pockers) > 0:
				t = r.randint(0, len(pockers)-1)
				card = pockers.pop(t)
				player[j].append(card)
			else:
				print("Nomore card.")
				break

def show_card():
	for name, card in player.items():
		print(str(name)+":")
		for i in card:
			print(i)

if __name__ == "__main__":
	#player initial
	player = {"player1":[], "player2":[], "player3":[], "player4":[]}
	#pocker initial
	pocker()
	giveCard()

	#lock initail
	Lock = threading.Lock()
	#thread initial
	threads = []
	for name in player:
		thread = myThread(name)
		thread.start()
		threads.append(thread)

	while not len(pockers) == 0:
		if win == 4:
			print("all player finish.")
			break
		while not card == None:
			pass
		print
		show_card()
		Lock.acquire()
		card = r.randint(0, len(pockers)-1)
		print("[CARD]:"+ str(pockers[card]))
		t0 = time.time()
		Lock.release()


	exitFlag = True

	for t in threads:
		t.join()
	print("End Game...")







