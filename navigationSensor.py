import sys, getopt

sys.path.append('.')
import RTIMU
import os.path
import time
import math

class NavigationSensor:

    __SETTINGS_FILE = "RTIMULib"

    def __init__(self):
        print("Using settings file " + SETTINGS_FILE + ".ini")
        if not os.path.exists(SETTINGS_FILE + ".ini"):
            print("Settings file does not exist, will be created")

        s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(s)

        print("IMU Name: " + imu.IMUName())

        if not self.imu.IMUInit():
            print("IMU Init Failed")
            sys.exit(1)
        else:
            print("IMU Init Succeeded")

        # this is a good time to set any fusion parameters

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.poll_interval = self.imu.IMUGetPollInterval()

    def get_compass_value(self):
        while True:
            if imu.IMURead():
                data = imu.getIMUData()
                fusionPose = data["fusionPose"]
                bearTo = math.degrees(fusionPose[2])
                time.sleep(self.poll_interval*1.0/1000.0)
                return bearTo