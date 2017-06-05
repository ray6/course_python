## 21 point server
import socket
import select
import sys
import random as r

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9999
cards = []
player = {}
flag = {}


def server():

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind((HOST, PORT))

	server.listen(5) # TCP listener
	SOCKET_LIST.append(server)
	player.setdefault(server, [])
	get_card(server, 2)

	while True:
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST,[],[],0)
		#a new connection request
		for sock in ready_to_read:
			if sock == server:
				sockfd, addr = server.accept()
				SOCKET_LIST.append(sockfd)
				player.setdefault(sockfd, [])
				flag.setdefault(sockfd, True)
				#give card
				get_card(sockfd, 2)
				sockfd.send("[House] : ( unseen ),"+str(player[server][1])+"\n[You] : "+str(player[sockfd])+"\nHit?(y/n)")

			else:
				try:
					data = sock.recv(RECV_BUFFER)
					if data:
						if flag[sock]:
							if data[0] == 'y' or data[0] == 'Y':
								get_card(sock, 1)
								point = count_point(player[sock])
								if point > 21:
									flag[sock] = False
									sock.send("[YOU] : "+str(player[sock]) + "\nGot " + str(point) + "point.\n Game over QQ\n")
									state = flag.values()
									player[sock] = False
									if state.count(True) == 0:
										sys.exit(final(server))
								elif len(player[sock]) >= 5:
									flag[sock] = False
									player[sock] = -1
									sock.send("Get 5 card , Please Wait.....\n")
									state = flag.values()
									if state.count(True) == 0:
										sys.exit(final(server))
								else:
									sock.send("[House] : ( unseen ),"+str(player[server][1])+"\n[You] : "+str(player[sock])+"\n"+str(point)+" point\nHit?(y/n)")
							elif data[0] == 'n' or data[0] == 'N':
								flag[sock] = False
								point = count_point(player[sock])
								player[sock] = point
								sock.send("You Get " + str(point) + " point.\n Please Wait.....\n")
								state = flag.values()
								if state.count(True) == 0:
									sys.exit(final(server))
							else:
								sock.send("Invalid input , Do you wanna Hit?(y/n)")
						else:
							sock.send("Please Wait.....\n")
					else:
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
						if player.has_key(sock):
							player[sock] = False
						if flag.has_key(sock):
							flag[sock] = False
						state = flag.values()
						if state.count(True) == 0:
							sys.exit(final(server))
				except:
					#player offline
					cast_to_all(server, sock, "Client (%s, %s) is offline\n" %addr)
					if sock in SOCKET_LIST:
						SOCKET_LIST.remove(sock)
					if player.has_key(sock):
						player[sock] = False
					if flag.has_key(sock):
						flag[sock] = False
					state = flag.values()
					if state.count(True) == 0:
						sys.exit(final(server))
					continue
	server.close()

def cast_to_all(server, sock, message):
	for socket in SOCKET_LIST:
		#send the msg only to peer
		if socket != server and socket !=sock :
			try:
				socket.send(message)
			except:
				#broken socket connection
				socket.close()
				#broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)
def final(server):
	cnt = 1
	cast_to_all(server, server, "Final Count......\n[House] : "+str(player[server][0])+","+str(player[server][1]))
	while count_point(player[server]) < 17:
		get_card(server, 1)
		cnt += 1
		cast_to_all(server, server, ","+str(player[server][cnt]))
	point = count_point(player[server])
	cast_to_all(server, server, "\n[House] : "+ str(point) + " point.\n")

	if point > 21 :
		for user, grade in player.items():
			if grade != False and user != server:
				user.send("You Win \n")

	elif len(player[server]) >= 5:
		for user, grade in player.items():
			if grade != False:
				user.send("House get 5 card, House Win.\n")

	else:
		for user, grade in player.items():
			if grade != False and user != server:
				if grade > point or grade == -1:
					user.send("[YOU] : " + str(grade) + " point.\n You Win \n")
				else:
					user.send("[YOU] : " + str(grade) + " point.\n You Lose QQ\n")


def make_card():
	for i in range(1,5):
		for j in range(1, 14):
			cards.append((i,j))

def get_card(user, num):
	for i in range(num):
		if len(cards) > 0:
			t = r.randint(0, len(cards)-1)
			card = cards.pop(t)
			player[user].append(card)
		else:
			print("Nomore card.\n")
			break

def count_point(card):
	point = 0
	ace = 0
	for c in card:
		if c[1] == 1:
			ace += 1
		elif c[1] >= 10:
			point += 10
		else:
			point += c[1]
	if point > 21 or ace == 0:
		point += ace
		return point
	elif ace == 4:
		if point <= 7:
			point += 14
		else:
			point+=4
		return point
	elif ace == 3:
		if point <= 8:
			point += 13
		else:
			point+=3
		return point
	elif ace == 2:
		if point <= 9:
			point += 12
		else:
			point += 2
		return point
	else:
		if point <= 10:
			point += 11
		else:
			point += 1
		return point


if __name__ == "__main__":
	make_card()
	server()
