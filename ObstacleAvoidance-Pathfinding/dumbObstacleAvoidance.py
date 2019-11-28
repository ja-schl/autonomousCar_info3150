# External module imports
import RPi.GPIO as GPIO
import time
import random
import sys

#Needed to import file located in different folder???
sys.path.insert(1, '../')

#from RTIMUScripts import get_heading
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

wheels = Motor()
frontSensor = Ultrasonic()
frontLeftSensor = InfraredSensor(21)
frontRightSensor = InfraredSensor(16)
backLeftSensor = InfraredSensor(12)
backRightSensor = InfraredSensor(20)

components = [wheels, frontSensor, backLeftSensor, frontLeftSensor, backRightSensor, frontRightSensor]

def randomLeftRight():
    if bool(random.getrandbits(1)) is True:
        wheels.turnRight()
        time.sleep(0.5)
        return "right"
    else:
        wheels.turnLeft()
        time.sleep(0.5)
        return "left"

def frontObstacle():
    if frontSensor.sense() <= 15.0:
        time.sleep(0.1)
        print ("FRONT BLOCKED")
        return True
    else:
        print ("FRONT CLEAR")
        return False

def ultrasonicDistance():
    ultrasonicDistance = frontSensor.sense()
    if frontSensor.latestValidUltrasonicDistance == 0:
        frontSensor.latestValidUltrasonicDistance = ultrasonicDistance
        return ultrasonicDistance
    if ultrasonicDistance - frontSensor.latestValidUltrasonicDistance > 50:
        motor.stop()
        ultrasonicDistance = waitForValidUltrasonicValue()
    frontSensor.latestValidUltrasonicDistance = ultrasonicDistance
    time.sleep(.05)
    return ultrasonicDistance

def frontRightObstacle():
    if frontRightSensor.is_blocked_by_obstacle():
        print ("FRONT RIGHT BLOCKED")
        return True
    else:
        print ("FRONT RIGHT CLEAR")
        return False

def frontLeftObstacle():
    if frontLeftSensor.is_blocked_by_obstacle():
        print ("FRONT LEFT BLOCKED")
        return True
    else:
        print ("FRONT LEFT CLEAR")
        return False

def backRightObstacle():
    if backRightSensor.is_blocked_by_obstacle():
        print ("BACK RIGHT BLOCKED")
        return True
    else:
        print ("BACK RIGHT CLEAR")
        return False

def backLeftObstacle():
    if backLeftSensor.is_blocked_by_obstacle():
        print ("BACK LEFT BLOCKED")
        return True
    else:
        print ("BACK LEFT CLEAR")
        return False

def obstacleAvoid():
    #Drive forward until obstacle ahead.
    while True:
        wheels.forward()

        if backRightObstacle() and frontObstacle():
            goBackTunnel("right")
            continue

        if backLeftObstacle() and frontObstacle():
            goBackTunnel("left")
            continue

        #If obstacle ahead, randomly turn either left or right.
        if frontObstacle():
            goAheadManeuver(randomLeftRight())
            continue

        if frontLeftObstacle():
            goBackManeuver("left")
            continue

        if frontRightObstacle():
            goBackManeuver("right")
            continue

        if frontObstacle() and frontLeftObstacle() and frontRightObstacle() and backLeftObstacle() and backRightObstacle():
            goBackTunnel("stuck")
            continue

#For going back long distances (e.g. in a  tunnel)
def goBackTunnel(obstacleDirection):
    counter = 0
    if obstacleDirection is "right":
        while backRightObstacle() or frontRightObstacle() and counter <= 10:
            wheels.backward()
            time.sleep(1)
            counter += 1
    elif obstacleDirection is "left":
        while backLeftObstacle() or frontLeftObstacle() and counter <= 10:
            wheels.backward()
            time.sleep(1)
            counter += 1

    #If surrounded by both sides, reverse all the way out and turn around
    else:
        while backLeftObstacle() or backRightObstacle():
            wheels.backward()
            time.sleep(1)
        if randomLeftRight() is "right":
            wheels.turnRight()
            time.sleep(5)
        else:
            wheels.turnLeft()
            time.sleep(5)

#For going back a short distance
def goBackManeuver(obstacleDirection):
    wheels.backward()
    time.sleep(0.5)

    if obstacleDirection is "right" and :
        wheels.turnLeft()
        time.sleep(0.5)
    else:
        wheels.turnRight()
        time.sleep(0.5)

def goAheadManeuver(turnDirection):
    # If turn direction is right, keep turning right until obstacle is cleared
    if turnDirection is "right":
        while frontObstacle() or frontLeftObstacle():
            wheels.turnRight()
    # If turn direction is left, keep turning left until obstacle is cleared
    else:
        while frontObstacle() or frontRightObstacle():
            wheels.turnLeft()


def cleanGPIO():
    print ("GPIO CLEANED")
    for component in components:
        del component


def main():
   obstacleAvoid()


if __name__ == "__main__":
    main()

try:
    main()
except KeyboardInterrupt:
    cleanGPIO()
    sys.exit()