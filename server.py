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
				print("game beginning")
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
			response = self.getmsg()
			if response == "I want to play":
				self.waitForOpponent()
				break	

	def sendmsg(self, sendstr):
		self.client.send(sendstr.encode('utf-8'))
	
	def getmsg(self):
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

		"""
		players receive "enter game".
		at this point they start taking turns.
		player 1 goes first.
		send him a "your turn" message.
		he responds with his play.
		receive it.

		if score == 5, send both players "game over". send player 1 "you win"

		send player 1 a message. it says "player 2 is going...."
		now, send player 2 "your turn".
		she responds with her play.
		receive it.

		if score == 5, send both players "game over" and send player 2 "you win"

		send her "player 1 is going..."


		okay, so the general pattern is,

		while 1:
		for each player:
			send "your turn"
			wait for play
			evaluate it
			send both players the play
			if game over: 
				send "game over" to both
				send "you win" to current player
				send "you lose" to other player
				end game (return)
			send "other guy is going" to current player.	


		"""

		while 1:
			for currPlayer in [self.p1, self.p2]:
				
				currPlayer.sendmsg("yourTurn " + str(self.score))
				
				play = currPlayer.getmsg() #halts

				if play == "add 1":
					self.score += 1
				elif play == "add 2":
					self.score += 2
				elif play == "sub 1":
					self.score -= 1
				#(its impossible for the client to send anything else.)

				self.sendtoboth("scoreIs " + str(self.score))

				if self.score == 5:
					self.sendtoboth("gameOver")
					sleep(.2)
					currPlayer.sendmsg("youWin")
					if currPlayer==self.p1:
						self.p2.sendmsg("youLose")
					else:
						self.p1.sendmsg("youLose")	
					return

				currPlayer.sendmsg("opponentGoing")	


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