class Agent:

    def __init__(self):
        self.isAlive = True
        self.goldPicked = 0
        self.action = None
        self.path = []
        self.currentLocation = None
        self.destination = None
        self.crashToWall = False
        self.hasMoved = False           # If agent need to return back to previous room, probably because of wall