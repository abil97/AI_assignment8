from __future__ import division
from __future__ import absolute_import
import random
from node import Room
from io import open
from monster import Monster
from agent import Agent

new_dict = {}
mons, hole, gold, wall, teleport, wind, smell = 0, 0, 0, 0, 0, 0, 0
listparam = [mons, wall, hole, gold, teleport, wind, smell]
main_dict = {}
changed = set()                                    # Set of rooms that were changed

agent = Agent()                                    # This is the agent

# Reset global variables
def resetGlobals():
    new_dict.clear()
    main_dict.clear()
    changed.clear()
    global globalClock,totalMonstersinTeleportRooms, agent, lock
    globalClock = [0]
    totalMonstersinTeleportRooms = [0]
    lock = [0]
    agent = Agent()

# This is used for loading the maze
def generate_pre_dictonary_2(lst):
    for el in lst:
        main_dict.update({el: []})
# This is used for creating the maze
# Generate an empty dictionary
def generate_pre_dictonary(lst):
    for el in lst:
        new_dict.update({el: []})

def print_dict(dict):
    for el in dict:
        stri = el.toString() + u": { "
        tmplst = dict[el]
        for val in tmplst:
            if val != tmplst[0]:
                stri += u", "
            stri += u"\"" + u"Room " + unicode(val.id) + u"\""
        stri += u" }"
        print stri

def print_list(lst):
    stri = u"["
    for el in lst:
        stri += u" \"" + el.toString() + u"\" "
    stri += u"]"
    print stri

def has_duplicates(listObj):
    return len(listObj) != len(set(listObj))

# Check if graph can be constructed with the given number of nodes and edges
def check(N, K, p, k):
    lst = []
    for i in xrange(N - K):
        lst.append(p)
    for i in xrange(K):
        lst.append(k)

    # If negative integer is present or sum is not even
    if min(lst) < 0 or (sum(lst) % 2 == 1):
        return False

    while (len(lst) > 0):

        lst.sort(reverse=True)
        x = lst.pop(0)

        if x == 0:
            return True
        if x < 0 or x > len(lst):
            return False

        for i in xrange(x):
            lst[i] -= 1

    return False

def distribute_items(lst):
    added = []
    cpy_mons = listparam[0]
    randints = range(1, cpy_mons + 1)
    emptyRooms = lst[:]

    # Time to distribute monsters!!!
    socialOrLoner = ["social", "loner"]
    #mmtype = random.choice(socialOrLoner)
    mmtype = "social"
    #print "ALL MONSTERS ARE " + mmtype.upper() + "S"
    while (cpy_mons > 0):

        tmp = random.choice(emptyRooms)

        monsId = randints.pop(0)
        monster = Monster(monsId)  # Create new monster object
        monster.type = mmtype
        tmp.monsters.append(monster)

        tmp.pres_monster = 1
        tmp.pres_smell = 1
        tmp.smellList.append(1)
        cpy_mons -= 1
        added.append(tmp)
        emptyRooms.remove(tmp)
    del cpy_mons

    # Time to distribute holes!
    cpy_holes = listparam[2]

    while (cpy_holes > 0):
        tmp = random.choice(emptyRooms)

        tmp.pres_hole = 1
        tmp.pres_wind = 1
        cpy_holes -= 1
        added.append(tmp)
        emptyRooms.remove(tmp)
    del cpy_holes

    # Time to distribute walls!
    cpy_walls = listparam[1]

    while (cpy_walls > 0):
        tmp = random.choice(emptyRooms)

        tmp.pres_wall = 1
        cpy_walls -= 1
        added.append(tmp)
        emptyRooms.remove(tmp)
    del cpy_walls

    # Time to distribute gold!
    cpy_gold = listparam[3]
    while (cpy_gold > 0):
        tmp = random.choice(emptyRooms)

        tmp.pres_gold = 1
        cpy_gold -= 1
        added.append(tmp)
        emptyRooms.remove(tmp)
    del cpy_gold

    # Time to distribute teleportation gates!
    added = []
    cpy_tg = listparam[4]
    while (cpy_tg > 0):
        tmp = random.choice(emptyRooms)

        tmp.pres_teleport = 1
        cpy_tg -= 1
        added.append(tmp)
        emptyRooms.remove(tmp)
    del cpy_tg

    # Place agent in random maze room
    tmp = random.choice(emptyRooms)

    global agent
    tmp.pres_agent = 1
    tmp.agent = agent
    agent.currentLocation = tmp
    agent.path.append(tmp)

def generate(N, K, p, k):
    normal = []
    border = []

    templist = range(1, N + 1)

    # Fill list of normal nodes
    for i in xrange(N - K):
        x = random.choice(templist)
        templist.remove(x)
        nroom = Room(x)
        nroom.isNormal = True
        nroom.conn_remained = p
        normal.append(nroom)

    # Fill list of border nodes
    for i in xrange(N - K, N):
        x = random.choice(templist)
        templist.remove(x)
        nroom = Room(x)
        nroom.isNormal = False
        nroom.conn_remained = k
        border.append(nroom)

    new_lst = normal + border
    generate_pre_dictonary(new_lst)
    copylst = new_lst[:]

    while (True):
        # This works!!!!
        new_lst.sort(key=lambda x: x.conn_remained, reverse=True)

        curr_node = new_lst.pop(-1)
        degree = curr_node.conn_remained

        if degree == 0 or len(new_lst) == 0:
            break

        toConnect = []
        for i in range(degree):
            toConnect.append(new_lst[i])

        for ngb in toConnect:
            new_dict[curr_node].append(ngb)
            new_dict[ngb].append(curr_node)
            curr_node.conn_remained -= 1
            ngb.conn_remained -= 1

            curr_node.neighbors.append(ngb)
            ngb.neighbors.append(curr_node)

    distribute_items(copylst)

def read_generator(file, sigma, omega):
    f = open(file, u"r+")  # open file
    count = 0  # count the number of lines ~ rooms
    room_list = []
    list_of_rooms_nbrs = []  # list of rooms neighbors is used to figure out what is maximum num of neighbors
    monster_total_count = 0
    for line in f:

        nline = line.split(":")
        rest = nline[1]
        id = int(nline[0])
        mm = int(rest[0])
        ww = int(rest[2])
        hh = int(rest[4])
        gg = int(rest[6])
        tt = int(rest[8])

        check_array = [mm, ww, hh, gg, tt]
        itr = 0
        for el in check_array:
            if el > 0:
                itr += 1
        if itr > 1:
            return "There is more than 1 item in the room\n"

        if mm > 0:
            monster_total_count += 1

        neighbors_list = line.split(u" ")
        neighbors_list.remove(neighbors_list[0])  # list with ids of current room's neighbors

        room = Room(id)
        room.pres_monster = mm
        room.pres_gold = gg
        room.pres_wall = ww
        room.pres_hole = hh
        room.pres_teleport = tt

        # print(neighbors_list)

        # Convert all ids to int
        for i in xrange(len(neighbors_list)):
            if neighbors_list[i] != "\n":
                neighbors_list[i] = int(neighbors_list[i])

        room.neighbors = neighbors_list[:]  # copy neighbor list

        # appending to the lists of rooms and neighbors
        room_list.append(room)
        list_of_rooms_nbrs.append(room.neighbors)

        count += 1
    # Get max number of neighbors
    max = 0
    for el in list_of_rooms_nbrs:
        if len(el) > max:
            max = len(el)

    # Figure out if room is normal or border
    for el in room_list:
        if len(el.neighbors) == max:
            el.isNormal = True
        else:
            el.isNormal = False

    # Adding monsters
    choose_type = ["loner", "social"]
    #types = random.choice(choose_type)
    types = "social"
    randints = range(1, monster_total_count + 1)
    listparam[0] = monster_total_count              # Set total monster number to global variable
    for el in room_list:
        if el.pres_monster == 1:
            id = randints.pop(0)
            monster = Monster(id)
            monster.type = types
            el.monsters.append(monster)
            el.pres_smell = 1
        if el.pres_hole == 1:
            el.pres_wind = 1

    # Add agent to the room
    for room in room_list:
        if room.pres_wall == 1 or room.pres_gold == 1 or room.pres_monster > 0 or room.pres_hole == 1:
            continue
        global agent
        room.agent = agent
        room.pres_agent = 1
        agent.currentLocation = room
        agent.path.append(room)
        agent.action = "Spawned"
        break

    generate_pre_dictonary_2(room_list)
    for el in room_list:
        for nl in room_list:
            if nl.id in el.neighbors:
                main_dict[el].append(nl)

def allocate_wind(graph, sigma, omega):
    # if sigma = 0; wind does not spread
    if sigma == 0 or omega <= 0:
        return
    # going through all graph elements
    for el in graph:
        if el.pres_hole == 0:  # if no wind in current room, move to next room
            continue
        bfs_wind(graph, el, sigma, omega)

def allocate_smell(graph, sigma, omega):
    # if sigma = 0; wind does not spread
    if sigma == 0 or omega <= 0:
        return
    # going through all graph elements
    for el in graph:
        if el.pres_monster == 0:  # if no smell in current room, move to next room
            continue
        bfs_smell(graph, el, sigma, omega)

# Calculate the minimum value for the smell given spread an decay
def calculate_limit(sigma, omega):
    res = 1
    for i in xrange(sigma):
        res *= omega
    return res

# These function was implemented using https://stackoverflow.com/a/46383689/9901274
# Allocate, spread wind using BFS
def bfs_wind(graph, start, sigma, omega):
    # print("Start is : {}".format(start.id))
    # keep track of all visited nodes
    explored = []
    # keep track of nodes to be checked
    queue = [start]

    levels = {}  # this dict keeps track of levels
    levels[start] = 0  # depth of start node is 0
    limit = calculate_limit(sigma, omega)

    visited = [start]  # to avoid inserting the same node twice into the queue
    new_wind = start.pres_wind
    # keep looping until there are nodes still to be checked
    while queue:
        # pop shallowest node (first node) from queue
        if new_wind < limit:
            return

        node = queue.pop(0)
        explored.append(node)
        neighbours = graph[node]
        new_wind = new_wind * omega
        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour not in visited:
                # HERE!!!
                if new_wind < limit:
                    return
                if new_wind > neighbour.pres_wind:
                    neighbour.pres_wind = new_wind
                queue.append(neighbour)
                visited.append(neighbour)

                levels[neighbour] = levels[node] + 1
                if levels[neighbour] > sigma:  # sigma defines 'depth'
                    return
            # print(neighbour, ">>", levels[neighbour])
    return explored

# These function was implemented using https://stackoverflow.com/a/46383689/9901274
# Allocate, spread smell using BFS
def bfs_smell(graph, start, sigma, omega):
    # print("Start is : {}".format(start.id))
    # keep track of all visited nodes
    explored = []
    # keep track of nodes to be checked
    queue = [start]

    levels = {}  # this dict keeps track of levels
    levels[start] = 0  # depth of start node is 0
    limit = calculate_limit(sigma, omega)

    visited = [start]  # to avoid inserting the same node twice into the queue
    new_smell = start.pres_smell
    # keep looping until there are nodes still to be checked
    while queue:
        if new_smell < limit:
            return

        # pop shallowest node (first node) from queue
        node = queue.pop(0)
        explored.append(node)
        neighbours = graph[node]
        new_smell = new_smell * omega
        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour not in visited:
                # HERE!!!
                if new_smell < limit:
                    return

                neighbour.smellList.append(new_smell)
                if new_smell > neighbour.pres_smell:
                    neighbour.pres_smell = new_smell
                    changed.add(neighbour)

                queue.append(neighbour)
                visited.append(neighbour)

                levels[neighbour] = levels[node] + 1
                if levels[neighbour] > sigma:  # sigma defines 'depth'
                    return

    return explored


# This works!
def reset_smell(dict):
    for room in dict:
        del room.smellList[:]
        if room.pres_monster >= 1:
            room.pres_smell = 1
            room.smellList.append(1)
            continue
        else:
            room.pres_smell = 0
            room.smellList.append(0)

# Write generated maze to the file
def output(file):

    for el in new_dict:
        if el.pres_smell < 1:
            el.pres_smell = 0
        if el.pres_wind < 1:
            el.pres_wind = 0

    global agent
    key = agent.currentLocation
    stri = unicode(key.id) + u": " + unicode(key.pres_monster) + u", " + unicode(key.pres_wall) + \
           u", " + unicode(key.pres_hole) + u", " + unicode(key.pres_gold) + \
           u", " + unicode(key.pres_teleport) + u", " + unicode(key.pres_wind) + \
           u", " + unicode(key.pres_smell) + \
           u": " + agent.action + "; "

    file.write(stri + "\n")

teleportRooms = []  # Set of rooms with teleports

globalClock = [0]
totalMonstersinTeleportRooms = [0]

def tick(dict, sigma, omega):

    if lock[0] == 0:
        return

    monstersMoved = 0
    changed.clear()                    # All rooms initially are NOT CHANGED
    # Return monsters back home from rooms with walls and holes
    # RETURNING MONSTERS START HERE!!!
    for currRoom in dict:
        # No need to return monstrers in the first cycle
        if globalClock[0] == 0:
            for room in dict:  # Fill the set of teleport rooms
                if room.pres_teleport == 1:
                    teleportRooms.append(room)
            break  # Exit the outer looooop!

        # EVERYTHING STARTS FROM HERE
        # If monsters need to return here
        if len(currRoom.monstersToReturn) > 0:

            while (len(currRoom.monstersToReturn) > 0):
                monster = currRoom.monstersToReturn.pop(0)

                if monster.killingAgent:
                    continue

                monster.hasMoved = True                 # Blocking monster for one cycle
                currRoom.monsters.append(monster)       # Return monster back
                currRoom.pres_monster += 1              # Update naumber of monsters
                changed.add(currRoom)
                monstersMoved += 1

                monster.path.append(currRoom)

        # If monsters need to move away from here (ROOM WITH HOLE OR WALL)
        if len(currRoom.monstersToLeave) > 0:
            while (len(currRoom.monstersToLeave) > 0):
                monster = currRoom.monstersToLeave.pop(0)

                if monster.killingAgent:
                    continue

                currRoom.monsters.remove(monster)
                currRoom.pres_monster -= 1
                changed.add(currRoom)

        # If monsters need to move away from here (Source Room with teleport)
        if len(currRoom.monstersToLeaveAfterTeleportation) > 0:
            for monster in currRoom.monstersToLeaveAfterTeleportation:

                if monster.isBlocked > 0:                       # If monster is blocked, skip it
                    continue
                if monster.killingAgent:
                    continue
                currRoom.deleteList.append(monster)             # Otherwise, it should be deleted

            for m in currRoom.deleteList:                       # Deleting monster from the room
                currRoom.monsters.remove(m)
                currRoom.monstersToLeaveAfterTeleportation.remove(m)
                currRoom.pres_monster -= 1
            del currRoom.deleteList[:]

            changed.add(currRoom)

        # Teleporting monster here  (DESTINATION ROOM WITH TELEPORT)
        if len(currRoom.teleportedMonsters) > 0:

            for monster in currRoom.teleportedMonsters:  # Iterating through all monsters that need to be teleported here

                # If all monsters are blocked, nothing to do here
                if monster.isBlocked > 0:
                    continue
                if monster.killingAgent:
                    continue

                monster.hasMoved = True
                currRoom.monsters.append(monster)       # Add monster to current room (Finally Teleported)
                currRoom.pres_monster += 1              # Add monster to current room (Finally Teleported)
                currRoom.deleteList.append(monster)

                changed.add(currRoom)
                monstersMoved += 1  # CAN THIS CAUSE ERROR???

                monster.path.append(currRoom)
                totalMonstersinTeleportRooms[0] += 1

            for m in currRoom.deleteList:
                currRoom.teleportedMonsters.remove(m)
            del currRoom.deleteList[:]

            changed.add(currRoom)

    # =========================================================================================================== #
    # Iterating throung maze rooms to make monsters move
    # This is "MAIN MOVING FUNCTION"
    for currRoom in dict:

        # if all monsters were moved, just stop
        if monstersMoved == listparam[0]:
            break
        # If there are several monsters in the room:
        if currRoom.pres_monster > 0:
            for monster in currRoom.monsters:

                # Iterating through all monsters in this room
                if monster.hasMoved:  # If monster has moved, skip this room
                    continue
                if monster.isBlocked > 0:  # If monster is blocked, skip this room
                    continue
                if monster.killingAgent:
                    continue
#
#============================================================================================================#
#

                # If monster has already visited some roooms
                if len(monster.path) != 0:

                    moveTo = monster.path[-1]

                    # Cant go back to wall, hole, monster. Cant teleport back, if he is in teleport room now
                    if moveTo.pres_wall == 1 or moveTo.pres_hole == 1 or \
                            moveTo.pres_monster > 0 or currRoom.pres_teleport == 1:

                        room = monster.path[-1]
                        while room == moveTo:                           # Choose random room which is not previous one
                            moveTo = random.choice(dict[currRoom])
                    else:
                        if monster.type == "social":
                            if (sum(moveTo.smellList) - 1 * omega) >= (sum(currRoom.pres_smell) - 1):
                                monster.path.pop(-1)
                            else:
                                room = monster.path[-1]
                                while room == moveTo:                   # Choose random room which is not previous one
                                    moveTo = random.choice(dict[currRoom])
                        elif monster.type == "loner":

                            moveTo.smellList.remove(1 * omega)
                            currRoom.smellList.remove(1)
                            perceiving_smell_moveTo = max(moveTo.smellList)
                            perceiving_smell_currRoom = max(currRoom.smellList)

                            if perceiving_smell_moveTo <= perceiving_smell_currRoom:
                                monster.path.pop(-1)
                            else:
                                room = monster.path[-1]
                                while room == moveTo:                   # Choose random room which is not previous one
                                    moveTo = random.choice(dict[currRoom])
                # If path is empty, move randomly
                else:
                    moveTo = random.choice(dict[currRoom])
#==================================================================================================================#

                # moveTo = random.choice(dict[currRoom])  # Randomly choosing destination room from its neighbors
                moveTo.pres_monster += 1                            # Increment number of monsters in the destination room
                moveTo.monsters.append(monster)                     # Move monster to the destination
                currRoom.deleteList.append(monster)
                monster.path.append(moveTo)                         # Add destination to the path

                # THIS WORKS
                if moveTo.pres_wall == 1 or moveTo.pres_hole == 1:

                    monster.hasMoved = True
                    currRoom.monstersToReturn.append(monster)
                    moveTo.monstersToLeave.append(monster)

                # THIS WORKS?
                elif moveTo.pres_teleport == 1:

                    monster.isBlocked = 2                                       # Block monster to wait 1 cycle
                    moveTo.monstersToLeaveAfterTeleportation.append(monster)    # Monster should be removed from here after one cycle
                    totalMonstersinTeleportRooms[0] += 1                        # Update total number of monsters in rooms with teleport

                    while True:                                                 # Select teleport room which is not equal to current one
                        teleportTo = random.choice(teleportRooms)
                        if teleportTo != moveTo:
                            teleportTo.teleportedMonsters.append(
                                monster)                                        # Add monster to destination room's teleported queue of monsters
                            break

                # THIS WORKS
                else:
                    monster.hasMoved = True

                monstersMoved += 1                      # Increment number of monsters moved
                changed.add(currRoom)
                changed.add(moveTo)

                if currRoom.pres_teleport == 1:
                    totalMonstersinTeleportRooms[0] -= 1

            # Deleting monster(s) from the current room
            for m in currRoom.deleteList:
                currRoom.monsters.remove(m)             # Remove monster from the current room
                currRoom.pres_monster -= 1              # Decrement number of monsters in the start
            del currRoom.deleteList[:]

    reset_smell(dict)

    # Unblock monsters in the end
    for currRoom in dict:

        # Set smell to 1 if any monster in the teleport room, otherwise 0
        if currRoom.pres_teleport == 1:
            if totalMonstersinTeleportRooms[0] == 0:
                currRoom.pres_smell = 0
            elif totalMonstersinTeleportRooms[0] > 0:
                currRoom.pres_smell = 1

        for m in currRoom.monsters:
            m.hasMoved = False          # All monsters are able to move now
            if m.isBlocked > 0:
                m.isBlocked -= 1        # Almost unblocked. Or finally unblocked

    globalClock[0] += 1

    allocate_smell(dict, sigma, omega)  # Reallocating smell, because monster is moving

lock = [0]
def moveAgent(agent, dict):

    if lock[0] == 0:
        currRoom = agent.currentLocation
        moveTo = random.choice(dict[currRoom])
        agent.destination = moveTo
        agent.action = "Move to " + unicode(moveTo.id)
        lock[0] = 1
        return


    currRoom = agent.currentLocation
    moveTo = agent.destination
    # Moving agent to the next room
    currRoom.pres_agent = 0
    currRoom.agent = None
    moveTo.pres_agent = 1
    moveTo.agent = agent

    # Change current location and extend travelled path
    agent.currentLocation = moveTo
    agent.path.append(moveTo)

    # Both initial room and destination have been changed
    changed.add(currRoom)
    changed.add(moveTo)


    currRoom = agent.currentLocation

    # Check end conditions
    if currRoom.pres_wall == 1:
        moveTo = agent.path[-2]
    else:
        moveTo = random.choice(dict[currRoom])  # Randomly choosing destination from neighbors

    moveTo.pres_agent = 1
    agent.destination = moveTo

    # Check agent's end conditions
    if agent.currentLocation.pres_hole == 1:
        agent.action = "Fall into hole"
        agent.isAlive = False
        return
    if agent.currentLocation.pres_monster > 0:
        agent.action = "Meet monster"
        agent.isAlive = False
        return
    if agent.currentLocation.pres_gold == 1:
        agent.action = "Pick up gold"
        agent.goldPicked += 1
        return

    # Simple moving action
    agent.action = "Move to " + unicode(moveTo.id)

def final_output_with_cycles(dict, sigma, omega, file):

    global agent
    # print_one_room(dict, agent.currentLocation)
    # output(file)
    while agent.isAlive and agent.goldPicked == 0:

        tick(dict, sigma, omega)
        moveAgent(agent, dict)
        print_one_room(dict, agent.currentLocation)
        output(file)

    # Print the very last cycle
    tick(dict, sigma, omega)
    changed.add(agent.currentLocation)


def main_input():
    while (True):
        inp = raw_input("To create a maze, type: initMaze N K k p M W H G T sigma omega\n"
                        "To load a maze, type: loadMaze filename sigma omega\n\n")
        sinp = inp.split()

        if sinp[0].lower() == "initMaze".lower():

            N, K, k, p, M, W, H, G, T, sigma, omega = int(sinp[1]), int(sinp[2]), int(sinp[3]), int(sinp[4]), \
                                                    int(sinp[5]), int(sinp[6]), int(sinp[7]), int(sinp[8]), \
                                                    int(sinp[9]), int(sinp[10]), float(sinp[11])
            if N <= K or p <= k:
                print u"Invalid number of nodes of edges. N should be > K, p should be > k\n"
                continue

            if check(N, K, p, k) == False:
                print("Maze cannot be constructed with these values of N, K, p, k. Try again\n")
                continue

            if M < 0 or W < 0 or H < 0 or G < 0 or T < 0:
                print("Number of items cannot be negative. Try again \n")
                continue
            if T < 2 and T > 0:
                print("Number of teleports cannot be less than 2. Try again\n")
                continue
            if M + W + H + G + T + 1> N:
                print("Total number of monsters, walls, holes and gold are greater than number of rooms. Try again \n")
                continue
            if sigma < 0 or omega < 0:
                print ("Spread and decay cannot be negative. Try again \n")
                continue
            if omega > 1:
                print ("Decay cannot be greater than 1. Try again.")
                continue
            listparam[0] = M
            listparam[1] = W
            listparam[2] = H
            listparam[3] = G
            listparam[4] = T
            listparam[5] = sigma
            listparam[6] = omega

            file = open("output.txt", "w+")
            file.truncate(0)
            for i in range(1, 10001):
                print ("***************************************************************************************************************")
                print ("Run #" + unicode(i) + "\n")
                file.write("Run #" + unicode(i) + "\n")
                generate(N, K, p, k)
                allocate_wind(new_dict, sigma, omega)
                allocate_smell(new_dict, sigma, omega)
                final_output_with_cycles(new_dict, sigma, omega, file)
                resetGlobals()
            break

        elif sinp[0].lower() == "loadMaze".lower():

            fname, sigma, omega = sinp[1], int(sinp[2]), float(sinp[3])

            if sigma < 0 or omega < 0:
                print ("Spread and decay cannot be negative. Try again \n")
                continue
            if omega > 1:
                print ("Decay cannot be greater than 1. Try again.")
                continue
            x = read_generator(fname, sigma, omega)
            if x == 'There is more than 1 item in the room\n':
                print x + ". Try again\n"
                main_dict.clear()
                continue
            file = open("output.txt", "w+")
            file.truncate(0)
            for i in range(1, 10001):
                print ("***************************************************************************************************************")
                print ("Run #" + unicode(i) + "\n")
                file.write("Run #" + unicode(i) + "\n")
                read_generator(fname, sigma, omega)
                allocate_smell(main_dict, sigma, omega)
                allocate_wind(main_dict, sigma, omega)
                final_output_with_cycles(main_dict, sigma, omega, file)
                resetGlobals()
            break
        else:
            print("Input cannot be recognized. Try again\n")
            continue

def print_maze(dict):
    print("\n")
    for key, value in dict.items():
        stri = u""
        stri = unicode(key.id) + u": " + unicode(key.pres_monster) + u", " + unicode(key.pres_wall) + u", " + unicode(
            key.pres_hole
        ) + u", " + \
               unicode(key.pres_gold) + u", " + unicode(key.pres_teleport) + u", " + unicode(
            key.pres_wind) + u", " + unicode(key.pres_smell) + u"     "

        for el in value:
            stri += unicode(el.id) + u" "
        stri += "   Number of Monsters: " + unicode(len(key.monsters)) + " " \
                "  Number of holes: " + unicode(key.pres_hole) + "   Number of agents: " + unicode(key.pres_agent) + u"    \n"
        print(stri)
    print("\n\n===================================================================\n\n")

def print_one_room(dict, key):

    global agent
    stri = u""
    stri = unicode(key.id) + u": " + unicode(key.pres_monster) + u", " + unicode(key.pres_wall) + u", " + unicode(key.pres_hole) + u", " + \
           unicode(key.pres_gold) + u", " + unicode(key.pres_teleport) + u", " + unicode(key.pres_wind) + u", " + unicode(key.pres_smell) + \
           u": " + agent.action + "; "

    # for el in dict[key]:
    #     stri += unicode(el.id) + u" "
    # stri += "   Number of Monsters: " + unicode(len(key.monsters)) + " " \
    #         + " Number of gold: " + unicode(key.pres_gold)  +  \
    #         "   Number of agents: " + unicode(key.pres_agent) + \
    #         "   Number of holes: " + unicode(key.pres_hole) + u"\n"
    print(stri)

main_input()

# initMaze 10 5 3 5 3 2 2 2 0 2 0.5 10
# initmaze 10 5 3 5 2 2 2 1 0 2 0.5