## 21 poiny player
import socket
import select
import sys

def client():
	if(len(sys.argv) < 3):
		print("Usage : python chat_client.py hostname port")
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect((host, port))
	except:
		print("unable to connect")
		sys.exit()

	print("============CASINO============")
	print("===========21 Point===========")
	sys.stdout.flush()
	#sys.stdout.write('[Me] '); sys.stdout.flush()

	while True:
		socket_list = [sys.stdin, s]

		#Get the list socket whicj are readable
		read_socket, write_socket, error_socket = select.select(socket_list, [], [])

		for sock in read_socket:
			if sock == s:
				#income msg from remote server, s
				data = sock.recv(4096)
				if not data:
					print("Bye Bye\n")
					sys.exit();
				else:
					sys.stdout.write(data)
					sys.stdout.flush()
					#sys.stdout.write('[Me] '); sys.stdout.flush()
			else:
				#user entered msg
				msg = sys.stdin.readline()
				s.send(msg)
				sys.stdout.flush()
				#sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
	sys.exit(client())
