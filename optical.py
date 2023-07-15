import datetime
import cv2
from modules import cfgHelper, distanceSensor, calibration, posEstimator, detector, lerp, pseyepy

### constants ###
CAM_GAIN = 0
CAM_EXPOSURE = 20
COLOR_LOW = (0, 0, 0)
COLOR_HIGH = (0, 0, 0)
COLOR_THRESH = 50
CAM_FOCALX = 554.2563
REAL_BALL_RADIUS = 2.25
CAM_FOCALD = 0

### initialization ###
cam = None
controller = None

### variables ###
rx, ry, rz = 0, 0, 0
lrx, lry, lrz = 0, 0, 0

### functions ###
def init(controller_, cam_):
    global controller, cam
    controller = controller_
    cam = cam_
    cam.gain = CAM_GAIN
    cam.exposure = CAM_EXPOSURE

def getCalibrationFrame():
    f, __ = cam.read()
    controller.UpdateSensors()
    return f, __

### program ###
def calibrate():
    global COLOR_LOW, COLOR_HIGH, CAM_FOCALD
    # Calibrate the color range using differences between 2 frames (1 with enabled controller, 2 with disabled controller)
    if cfgHelper.doIfNotExists("config/saveData.cfg"):
        print("Started blinking calibration")
        blinkingCalResult = calibration.blinkingCalibration(getCalibrationFrame, 500, controller.UpdateColor)
        COLOR_LOW = tuple(blinkingCalResult - COLOR_THRESH)
        COLOR_HIGH = tuple(blinkingCalResult + COLOR_THRESH)
        cfgHelper.save("config/saveData.cfg", f"{COLOR_LOW}|{COLOR_HIGH}")
    else:
        data = cfgHelper.read("config/saveData.cfg").split("|")
        COLOR_LOW = eval(data[0])
        COLOR_HIGH = eval(data[1])

    # Calculate the focal length of the camera for distance detection
    if cfgHelper.doIfNotExists("config/saveData2.cfg"):
        print("Started distance calibration")
        CAM_FOCALD = distanceSensor.computeFocal(20, REAL_BALL_RADIUS, getCalibrationFrame, COLOR_LOW, COLOR_HIGH)
        cfgHelper.save("config/saveData2.cfg", f"{CAM_FOCALD}")
    else:
        data = cfgHelper.read("config/saveData2.cfg")
        CAM_FOCALD = float(data)

print(f"Started PSMove tracker on {datetime.datetime.now().strftime('%H:%M:%S')}")
def loop(ho):
    global rx, ry, rz, lrx, lry, lrz
    frame, _ = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    controller.UpdateSensors()

    # Tracking using ball detection
    (x, y), radius = detector.detectBall(frame, COLOR_LOW, COLOR_HIGH)
    x = int(x)
    y = int(y)
    radiusf = radius
    radius = int(radius)

    # Approximating the 3D position of the controller
    if radius > 0:
        rx, ry, rz = lerp.posFilter(
            (lrx, lry, lrz),
            posEstimator.estimatePos(
                x,
                y,
                distanceSensor.dist(
                    radiusf,
                    REAL_BALL_RADIUS,
                    CAM_FOCALD
                ),
                CAM_FOCALX,
                frame.shape
            )
        )
        lrx, lry, lrz = rx, ry, rz

        # Draw the results
        # frame = cv2.circle(frame, (x, y), radius, (255, 255, 255), 2)
        frame = cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)
        frame = cv2.putText(frame, f"{rx:.2f},{ry:.2f},{rz:.2f}", (x + radius, y + radius), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255))
        frame = cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)
        frame = cv2.putText(frame, f"{ho.x:.2f},{ho.y:.2f},{ho.z:.2f}", (0, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 255, 255))

    cv2.imshow("CVMoveTracker", frame)
