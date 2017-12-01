from __future__ import print_function
import random
from team import Team
import time


def main():
    # Network variables
    dilationFactor = 7
    networkSize = 2

    print("Hello from the Network Mode")
    transmission_init = True
    # teamNumber = int(raw_input("What team are you?"))
    teamNumber = 0
    team = Team(teamNumber, UDP=False, dilationFactor=dilationFactor, networkSize=networkSize)
    timeout = random.uniform(5, 10)
    startTime = time.time()
    timePassed = 0
    while not team.checkFinished() and timePassed < 120:
        result, controlPacket = team.waitControl(timeout)
        # If result is 0 it means that timeout passed
        if result == 1:
            transmission_init = False
            team.receiver(controlPacket)
            timeout = (0.05 + random.uniform(0, 0.01))*dilationFactor
        if team.nextPlayer:
            print("I am the next player, sender mode...")
            if transmission_init:
                transmission_init = False
                team.sender(0)
            else:
                team.sender(0.001*dilationFactor)
            timeout = (0.1 + random.uniform(0, 0.02))*dilationFactor
        timePassed = time.time() - startTime

    if timePassed > 120:
        print("Timeout!")
    else:
        print("Transmission complete. Time elapsed: {}".format(timePassed))


if __name__ == "__main__":
    main()
