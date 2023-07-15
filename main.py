import modules.MoveController.MoveCore as move
import modules.pseyepy as pseyepy
import cv2
import orientation
import corrections
import optical
import glm
import udpHandler
import inputHandling

CONTROLLER_HALF_LENGTH = 9.5
HEAD_OFFSET = glm.vec3()
rx, ry, rz = 0, 0, 0

PSMOVE = move.MoveController()
cam = pseyepy.Camera(fps=60, resolution=pseyepy.Camera.RES_LARGE, hflip=True, auto_gain=False, auto_exposure=False)
PSMOVE.UpdateColor(True)
optical.init(PSMOVE, cam)
orientation.init(PSMOVE)
inputHandling.init(PSMOVE)
optical.calibrate()
orientation.calibrate()

while True:
    # loop each module
    optical.loop(HEAD_OFFSET)
    orientation.loop()

    # input handling
    if inputHandling.loop(): HEAD_OFFSET = glm.vec3(rx, ry, rz)

    # maths
    rx, ry, rz = optical.rx, optical.ry, optical.rz
    qx, qy, qz, qw = orientation.rq.x, orientation.rq.y, orientation.rq.z, orientation.rq.w
    rx, ry, rz = corrections.correctBallOffset(glm.vec3(rx, ry, rz), glm.quat(qw, qx, qy, qz), glm.vec3(0, 1, 0), CONTROLLER_HALF_LENGTH)
    rx, ry, rz = rx / 100, ry / 100, rz / 100
    rxc, ryc, rzc = corrections.headOffsetCorrection(glm.vec3(rx, ry, rz), glm.vec3(HEAD_OFFSET))

    # UDP handling
    # pos1,rot1,pos2,rot2,a,b,x,y,j1x,j1y,j2x,j2y,trig1,trig2,grip1,grip2,am1,am2,j1c,j2c,s1,s2
    # RIGHT HAND:
    # msg = f"-5|0|-0.5|1|0|0|0|{rxc}|{ryc}|{rzc}|{qw}|{qx}|{qz}|{qy}|0|0|0|0|0|0|0|{float(PSMOVE.buttons.cross)}|0|{PSMOVE.trig}|0|0|0|{int(PSMOVE.buttons.square)}|0|{int(PSMOVE.buttons.move)}|0|0"
    msg = f"{rxc}|{ryc}|{rzc}|{qw}|{qx}|{qz}|{qy}|5|0|-0.5|1|0|0|0|0|0|0|0|0|{float(PSMOVE.buttons.cross)}|0|0|{PSMOVE.trig}|0|0|0|{int(PSMOVE.buttons.square)}|0|{int(PSMOVE.buttons.move)}|0|0|0"
    print(msg)

    udpHandler.send(msg)

    # exit handling
    if cv2.waitKey(1) & 0xFF == 27:
        cv2.destroyAllWindows()
        break

cam.end()
