import time
import glm
import modules.MadgwickAHRS
import modules.IMUCalibration

import numpy as np
BETA = 0.035  # Beta value for the Madgwick algorithm. Change if needed.
UDP_IP = "localhost"
UDP_PORT = 49000
PSMOVE = None
lastFrame = 0
gyroOffset = 0

def init(controller_):
    global PSMOVE, lastFrame
    PSMOVE = controller_
    lastFrame = time.time()

def get():
    g_ = (PSMOVE.gyro.x, PSMOVE.gyro.y, PSMOVE.gyro.z)  # INPUT VALUES HERE
    a_ = (PSMOVE.acc.x, PSMOVE.acc.y, PSMOVE.acc.z)  # INPUT VALUES HERE
    return glm.vec3(g_), glm.vec3(a_)

def getG():
    PSMOVE.UpdateSensors()
    return PSMOVE.gyro.x, PSMOVE.gyro.y, PSMOVE.gyro.z

initialRot = glm.quat(0.7071069, 0.7071067, 0, 0)
# q90 = glm.quat(0.7071069, -0.7071067, 0, 0)
q90 = glm.quat(1, 0, 0, 0)
rq = None

forward = np.array([0, 0, 1])
up = np.array([0, 1, 0])
right = np.array([1, 0, 0])
transform_matrix = np.eye(4)
transform_matrix[:3, :3] = np.column_stack((right, up, -forward))

running = True
ahrs = modules.MadgwickAHRS.MadgwickAHRS(initialRot)
SLEEP = 1 / 240

def calibrate():
    global gyroOffset
    gyroOffset = glm.vec3(modules.IMUCalibration.CalibrateGyroscope(5000, getG))

def loop():
    global lastFrame, rq
    dt = time.time() - lastFrame
    PSMOVE.UpdateSensors()
    print(f"New sensor frame: {dt:.3f}s elapsed")

    g, a = get()
    ahrs.update(g - gyroOffset, a, BETA, dt)
    rq = glm.quat(tuple(np.dot(transform_matrix, ahrs.q * q90)))

    lastFrame = time.time()
    time.sleep(SLEEP)
