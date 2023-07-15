import time
import cv2
import glm
import numpy as np

def blinkingCalibration(getFrame, interval, changeColorF):
    lastColorChange = time.time() + interval / 1000
    frame0 = [None, False]  # frame, hasFrame
    frame1 = [None, False]  # frame, hasFrame
    result = None
    colorStatus = True
    completed = False
    changeColorF(True)
    while not completed:
        frame, _ = getFrame()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # blink
        if time.time() > lastColorChange + interval / 1000:
            if colorStatus:
                # light goes on
                frame0[0] = frame.copy()
                frame0[1] = True
            else:
                # light goes off
                frame1[0] = frame.copy()
                frame1[1] = True

            colorStatus = not colorStatus
            changeColorF(colorStatus)
            lastColorChange = time.time()

        # has both frames?
        if frame0[1] and frame1[1]:
            diff = cv2.absdiff(frame0[0], frame1[0])
            diffGray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            mask = cv2.bitwise_not(cv2.threshold(diffGray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1])
            rect = cv2.boundingRect(mask)
            croppedFrame = frame0[0][rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])]
            average = croppedFrame.mean(axis=(0, 1))
            img = np.zeros((512, 512, 3), np.uint8)
            img[:, :] = average
            print(average)

            result = glm.vec3(average)
            completed = True

        if cv2.waitKey(1) & 0xFF == 27:
            break

        cv2.imshow("Blinking Calibration", frame)
    cv2.destroyWindow("Blinking Calibration")
    return result
