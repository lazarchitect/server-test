import socket
from threading import Thread
from time import sleep

waitingroom = []

print("Opening Socket....")
print("Listening for incoming connections....")

class gameCreatorThread(Thread):
	def __init__(self):
		super().__init__()

	def run(self):
		global waitingroom
		while 1:
			print(waitingroom)
			sleep(1)
			if len(waitingroom) > 1:
				print("holy dickballs batman!")
				player1 = waitingroom[0]
				player2 = waitingroom[1]
				g = game(player1, player2)
				g.run()
				waitingroom = waitingroom[2:]

class clientThread(Thread):

	def __init__(self, c, a):
		super().__init__()
		self.client = c
		self.address = a
		self.waiting = False

	def run(self):
		while 1:
			response = self.readinput()
			print(self, "response is " + response)
			if response == "I want to play":
				self.waitForOpponent()

	def sendmsg(self, sendstr):
		self.client.send(sendstr.encode('utf-8'))
	
	def readinput(self):
		return self.client.recv(1024).decode("utf-8")

	def waitForOpponent(self):
		global waitingroom
		waitingroom.append(self)
		self.waiting = True

class game:
	#create a new game with these players.
	#these players are clientThreads.
	#you can send a message to them as a string.
	def __init__(self, p1, p2):
		self.p1 = p1
		self.p2 = p2
		self.score = 0

	def sendtoboth(self, sendstr):
		self.p1.sendmsg(sendstr)
		self.p2.sendmsg(sendstr)

	def run(self):
		self.sendtoboth("enter game")
		self.p1.waiting = False
		self.p2.waiting = False

		
		while 1:
			self.p1.sendmsg("your turn")
			move = self.p1.readinput()
			if move == "add 1":
				score += 1
			elif move == "add 2":
				score += 2
			elif move == "sub 1":
				score -= 1
			elif move == "game over":
				return;

			self.p2.sendmsg("your turn")
			move = self.p2.readinput()
			if move == "add 1":
				score += 1
			elif move == "add 2":
				score += 2
			elif move == "sub 1":
				score -= 1
			elif move == "game over":
				return;



def main():
	global waitingroom
	host = ''
	port = 50000
	backlog = 5 
	size = 1024 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	s.bind((host, port)) 
	s.listen(backlog)

	gameCreatorThread().start() #watches the waitingroom
	
	while 1: 
		client, address = s.accept() #stay listening booboo
		print("Client connection accepted.")
		handler = clientThread(client, address)
		handler.start()


if (__name__ == "__main__"):
	main()