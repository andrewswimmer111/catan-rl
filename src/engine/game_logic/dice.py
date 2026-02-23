import random 

def roll_dice():
    """
    Rolls 2 dice and adds their values.
    """
    r1 = random.randint(1, 6)
    r2 = random.randint(1, 6)
    return r1 + r2