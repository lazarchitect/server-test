import socket 

host = 'localhost' 
port = 50000 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port)) 

def sendmsg(sendstr):
	s.send(sendstr.encode('utf-8'))

def getmsg():
	return s.recv(1024).decode('utf-8')	

def killServer():
	s.send("kill".encode('utf-8'))

def getNumberInput():
	try:
		return int(input(">> "))
	except ValueError:
		print("pick a number, dumbo.")
		return getNumberInput()


################################################################

def splash():
	print("Choose option:")
	print("1: kill server")
	print("2: play score goal game")

	choice = getNumberInput()

	funcs = {1: killServer, 2: waitForSGGame}

	try:
		funcs[choice]()
	except IndexError:
		print("pick a number, dumbo.")
		splash()			

def waitForSGGame():
	sendmsg("I want to play")
	
	print("Waiting for Game.........\n\n\n")
	
	while 1:
		response = getmsg()
		print(response)
		if response == "enter game":
			scoreGoalGame()

def scoreGoalGame():

	print("You are now in the game.\n")
	print("the goal is to get to 5.")
	score = 0
	
	while 1:

		while getmsg() != "your turn":
			pass

		print("options:")
		print("1: add 1")
		print("2: add 2")
		print("3: subtract 1")

		choice = getNumberInput()

		breakloop = False

		while breakloop == False:
			if choice == 1:
				sendmsg("add 1")
				breakloop = True
				score+=1
			elif choice == 2:
				sendmsg("add 2")
				breakloop = True
				score+=2
			elif choice == 3:
				sendmsg("sub 1")
				breakloop = True
				score-=1
			else: choice = getNumberInput()	

		print("score is", score)

		if score == 5:
			print("you win! :)")
			sendmsg("game over")	
			exit()

		print("opponent is going")

		response = getmsg()

		if response == 1:
			score+=1
		if response == 2:
			score+=2
		if response == 3:
			score-=1		

		print("score is", score)

		if score==5:
			print("you lose! :(")
			sendmsg("game over")
			exit()

		print("okay, your turn.")


if __name__=="__main__":
	splash()