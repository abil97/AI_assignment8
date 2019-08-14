class Monster:

    isBlocked = 0
    hasMoved = False
    killingAgent = False

    def __init__(self, id):
        self.id = id
        self.type = ""
        self.path = []                      # Path of rooms travelled

    def toString(self):
        return "Monster " + unicode(self.id)