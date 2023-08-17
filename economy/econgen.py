from random import randint
from enum import Enum



def random_balance():
    """Generate some random amount of donuts"""
    return randint(1, 200)


def random_messages_gen():
    """Generate a random message to say during begging"""
    return randint(1, 5)


class BegMsg(Enum):
    m1 = "While cleaning the shrine you found {} Donut(s)"
    m2 = "While praying to the kitsune you got blessed with {} Donut(s)"
    m3 = "You were walking through the forest and found a box with {} Donut(s)"
    m4 = "Hana left you {} Donut(s) to eat"
    m5 = "You sent out the kitsune to hunt and she came back with {} Donut(s)"