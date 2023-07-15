import numpy as np

def CalibrateGyroscope(samples, getGyro):
    print("-"*50)
    print('Gyro Calibrating - Keep the IMU Steady')
    mpu_array = []
    gyro_offsets = [0, 0, 0]
    while len(mpu_array) < samples + 1:
        wx, wy, wz = getGyro()

        mpu_array.append([wx, wy, wz])
        print("Sample " + str(len(mpu_array)) + " " + str((wx, wy, wz)))
    for qq in range(0, 3):
        gyro_offsets[qq] = np.mean(np.array(mpu_array)[:, qq])
    print('Gyro Calibration Complete')
    return gyro_offsets
