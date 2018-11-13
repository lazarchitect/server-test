import socket 

host = 'localhost' 
port = 50000 
size = 1024 
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host,port))
except:
	print("\n-----------------------------\nServer could not be reached.\n-----------------------------\n")
	exit()

def sendmsg(sendstr):
	s.send(sendstr.encode('utf-8'))

def getmsg():
	return s.recv(1024).decode('utf-8')	

def getNumberInput():
	try:
		return int(input(">> "))
	except ValueError:
		print("pick a number, dumbo.")
		return getNumberInput()

def quit():
	exit()

################################################################

def mainMenu():
	print("Choose option:")
	print("1: play score goal game")
	print("2: quit")

	choice = getNumberInput()

	funcs = {1: waitForSGGame, 2: quit}

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

#runs the game
#only valid things to send to server are:
	#add 1
	#add 2
	#sub 1
	#game over
#the client does NOT keep a copy of the score. too wacky. just read it in each time.	
def scoreGoalGame():

	"""
	Basic idea: wait for server instructions. React differently based on what the server says.
	Possibilities:
		"yourTurn" + score:
			parse last token, print the score
			give player options
			wait for player to make a play
			send it to server

		"scoreIs " + score: DONE
			parse last token, print the score.

		"gameOver": DONE
			print "game over".

		"youWin": DONE
			print("you win")
			exit the game, call mainMenu() again.
		
		"youLose": DONE
			print("you lose")
			exit the game, call mainMenu() again

		"opponentGoing": DONE
			print that

	"""

	print("You are now in the game.\n")
	print("the goal is to get to 5.")
	

	while 1:
		instruction = getmsg()
		tokens = instruction.split(" ")
		print("tokens is", tokens)
		
		if tokens[0] == "yourTurn":
			print("your turn. Score is " + tokens[len(tokens)-1])

			print("Enter a number to make that move:")
			print("1: add 1")
			print("2: add 2")
			print("3: sub 1")

			userinput = getNumberInput()
			while userinput not in [1, 2, 3]:
				print("enter a valid number. options are 1, 2, and 3.")
				userinput = getNumberInput()

			if userinput == 1:
				sendmsg("add 1")
			elif userinput == 2:
				sendmsg("add 2")
			elif userinput == 3:
				sendmsg("sub 1")			

		if tokens[0] == "scoreIs":
			print("Score is " + tokens[len(tokens)-1])
		
		if tokens[0] == "gameOver":
			print("Game over!")
		
		if tokens[0] == "youWin":
			print("You win!")
			break
		
		if tokens[0] == "youLose":
			print("You lose :(")
			break
		
		if tokens[0] == "opponentGoing":
			print("Your opponent is going now.")

	input("<Enter> to go back to the main menu.")	
	mainMenu()	
		


if __name__=="__main__":
	mainMenu()










