import random

class Dice():

    def getRoll(self):
        r1 = random.randint(1, 6)
        r2 = random.randint(1, 6)
        return r1 + r2
