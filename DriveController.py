import sys
sys.path.insert(1, './Library/scripts')

from RTIMUScripts import get_heading
from motor import Motor
from infraredSensor import InfraredSensor
from ultrasonic import Ultrasonic

motor = Motor()
right_ir_sensor = InfraredSensor(16)
left_ir_sensor = InfraredSensor(12)
right_front_ir_sensor = InfraredSensor(20)
left_front_ir_sensor = InfraredSensor(21)
ultrasonicSensor = Ultrasonic()

components = [motor, right_ir_sensor, left_ir_sensor, right_front_ir_sensor, left_front_ir_sensor, ultrasonicSensor]

def noObstacleAtFront():
    return ultrasonicSensor.sense() > 10.01

def driveBackwards():
    motor.backward()

def turnStarted():
    while ultrasonicSensor.sense() < 15:
        print("Obstacle in front, keep turning")
    print("no obstacle in front, stop turning")
    motor.stop()
    startDriving()

def check_sides():
    if not right_ir_sensor.is_blocked_by_obstacle() and not right_front_ir_sensor.is_blocked_by_obstacle():
        motor.turnRight()
    elif not left_ir_sensor.is_blocked_by_obstacle() and not left_front_ir_sensor.is_blocked_by_obstacle():
        motor.turnLeft()
    elif right_ir_sensor.is_blocked_by_obstacle() and not right_front_ir_sensor.is_blocked_by_obstacle():
        motor.turnRight()
    elif left_ir_sensor.is_blocked_by_obstacle() and not left_front_ir_sensor.is_blocked_by_obstacle():
        motor.turnLeft()
    elif not right_ir_sensor.is_blocked_by_obstacle():
        motor.turnRight()
    elif not left_ir_sensor.is_blocked_by_obstacle():
        motor.turnLeft()
    else:
        print("Stopped due dead end")
        for component in components:
            del component

    turnStarted()

def check_for_FrontObstacle():
    while True:
        if not noObstacleAtFront():
            print("obstacle in front detected")
            motor.stop()
            check_sides()

def driveForward():
    motor.forward()
    check_for_FrontObstacle()

def startDriving():
    print("Start driving")
    print("obstacle at the front: " + str(noObstacleAtFront()))
    if noObstacleAtFront():
        driveForward()
    else:
        check_sides()

try:
    startDriving()
except KeyboardInterrupt:
    car_stopped = True
    print ("Stopped by User")
    for component in components:
        del component