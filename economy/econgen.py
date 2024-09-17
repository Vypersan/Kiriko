from random import randint
from enum import Enum



def random_balance():
    """Generate some random amount of donuts"""
    return randint(1, 200)

def random_messages_gen():
    """Generate a random message to say during begging"""
    return randint(1, 5)

def coinflip():
    """Output either 1 or 2"""
    return randint(1, 2)

def random_mission_loss():
    """Generate random donuts to lose when failing a `mission`"""
    return randint(50, 1000)

def random_mission_won():
    """Generate random donuts to win when succeeding in a mission."""
    return randint(100, 10000)

def mission_won_text():
    """Return random mission won text"""
    return randint(1, 2)

def mission_loss_text():
    """Return random mission loss text"""
    return randint(1, 2)

def mission_result():
    """Random result of mission"""
    return randint(1, 2)

class BegMsg(Enum):
    m1 = "While cleaning the shrine you found {} Donut(s)"
    m2 = "While praying to the kitsune you got blessed with {} Donut(s)"
    m3 = "You were walking through the forest and found a box with {} Donut(s)"
    m4 = "Hana left you {} Donut(s) to eat"
    m5 = "You sent out the kitsune to hunt and she came back with {} Donut(s)"


class MissionsWon(Enum):
    m1 = "You went towards a hashimoto boat to sink it, you did so successfully and recieved {} Donut(s)"
    m2 = "You snuck behind the hashimoto's backline and flanked them all! You received {} Donut(s) as a reward."
    m3 = ""
    m4 = ""
    m5 = ""
    m6 = ""
    m7 = ""
    m8 = ""
    m9 = ""
    m10 = ""

class MissionsLost(Enum):
    m1 = "You went towards a hashimoto boat to sink it, but you got caught and had to pay {} Donut(s) for your release."
    m2 = "You snuck behind the hashimoto's backline but they noticed and you got wounded. You payed  {} Donut(s) to the hospital for your recovery."
    m3 = ""
    m4 = ""
    m5 = ""
    m6 = ""
    m7 = ""
    m8 = ""
    m9 = ""
    m10 = ""