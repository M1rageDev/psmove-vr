import cv2
import modules.detector as dtc

def dist(radius, realRadius, focal):
    return (realRadius * focal) / radius

def computeFocal(realDistance, realRadius, getFrame, colorL, colorH):
    result = 0
    while True:
        frame, _ = getFrame()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if cv2.waitKey(1) & 0xFF == ord('e'):
            (_, __), radius = dtc.detectBall(frame, colorL, colorH)
            result = (radius * realDistance) / realRadius
            break

        t = f"Put the controller {realDistance}cm away from the camera lens and press E"
        (Twidth, Theight), Tb = cv2.getTextSize(t, cv2.FONT_HERSHEY_SIMPLEX, 0.5, None)
        frame = cv2.putText(frame, t, (0, Theight + Tb), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

        cv2.imshow("Distance calibration", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()
    return result
