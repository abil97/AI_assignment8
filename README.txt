Assingment 8. 10/11/18
======================================================

General notes:
======================================================

GENERAL NOTE: all instructions almost the same as in assignment7. 
		Main chages are:
				- There is no parameter for number of clock cycles anymore. Program will execute while agent is alive or has not picked up gold


- This program executes the instructions given in the assignment8
- This program is an updated and upgraded version of program used in the last assignment
- Some algorthms were updated as well as bugs and errors were fixed
- All code was written by myself only. I did not use anybody's else code
- When constructing a maze, there are 11 parameters to input: N,K,k,p,M,H,W,G,T,sigma,omega
	As before:	N - Number of rooms totally
			K - Number of border rooms
			k - Number of connections of ordinary rooms
			p - Number of connections of border rooms
			M - Number of monsters
			H - Number of holes
			W - Number of walls
			G - Number of gold
			T - Number of teleports
			sigma - denotes spread.
			omega - denoted decay. 

	Greek symbols of sigma, omega, and tau: σ, ω are not supported in Python 2.7 because they are Non-ASCII characters. 
	Because of that their names are written manually

- Number of rooms and their connections should satisfy following conditions: N > K, p > k. Otherwise error will be returned
- Program uses Havel-Hakimi algorithm to check if it is possible to create a maze with the following input. If it isn't possible, error will be returned
	- In the maze all items (monsters, walls , holes, gold, teleports) are distributed in a way such that:
	- No more than 1 item in each room
	- However, two monsters can be in one room
	- M + W + H + G + T + 1 < N. Otherwise error will be thrown. Because of agent we add +1 to overall number of items
	- Number of any item cannot be negative
	- Number of teleports cannot be less than 2. One teleport in total makes no sense and an error will be thrown

- Spread and decay cannot be negative. Also decay should be <= 1, otherwise smell will increase, which makes no sense. An error will be thrown in such case
- Decay is implemented in such way that it should not be > 1. For example, if decay is 0.5, each consequent room will be multiplied by 0.5. 
- Monsters can be of two types: loner and social, which is selected randomly. For this assignment, all monsters will be "socials"
- Agent starts its path in random maze room, which does not contains any other items
- Agent moves randomly
- Each agents' next action is recorded and printed in current step. For example, if agent is in the Room #2 and in the next cycle he will move to Room #3, his current action will be "Move to 3".
- If agent meets monster, finds gold or enters the room with hole, program execution stops
- Program runs 10000 times
- All input parameters are entered only once. Next, program will make 10000 runs with same parameters.
- Each run maze will be regenerated as well as all its items (monsters, holes, etc.). But input parameters will be the same
- Program prints output to console and to file output.txt


 
======================================================

Running the program
======================================================

1. There is a folder in the archive: assignment7. It could be extracted in any directory
2. In the terminal, change the directory to assignment7
3. In the terminal, type: python maze.py
4. If you want to create the maze, type: initMaze N K k p M W H G T sigma omega
	- "initMaze" is case insensitive
	- 10000 runs will be printed to console
	- Also, output will be printed to file output.txt. 
5. If you want to load the maze, type: loadMaze filename sigma omega
	- filename is assumed to be input.txt .However, it can be any text file in current directory.
	- The format of the maze to be read from the file, should be as specified in the assignment: id:M,W,H,G,T,w,s connected_rooms
	- Agent is added later, after maze have been read

			General format: 	id:M,W,H,G,T,w,s connected_rooms
			1. There should be no spaces if this part: id:M,W,H,G,T,w,s
			2. Connected_rooms should be separated by space
			Otherwise, input will not be read correctly
			3. Wind and smell should be initially set to 0.			

			Example of correct input: 
			
			9:0,0,0,0,0,0,0 4 2 10 6 7
			7:0,0,1,0,0,0,0 3 2 9 5 1
			1:0,0,1,0,0,0,0 8 7 6
			3:1,0,0,0,0,0,0 5 7 6
			2:0,1,0,0,0,0,0 8 9 7
			6:0,1,0,0,0,0,0 3 10 9 1 5
			4:1,0,0,0,0,0,0 8 9 5
			8:0,0,0,0,0,0,0 4 2 10 5 1
			10:0,0,0,0,0,0,0 6 8 9
			5:0,0,1,0,0,0,0 3 4 8 7 6 

6. Only room with agent will be printed

-

=========================================================

Contact info:
=========================================================

Author: Abil' Kuatbayev
Email: abil.kuatbayev@nu.edu.kz
