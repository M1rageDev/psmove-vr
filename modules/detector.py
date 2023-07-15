import cv2

def detectBall(frame, colorL, colorH):
    # Gaussian bluring the frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    # Constructing a mask for the controller's color range
    mask = cv2.dilate(cv2.erode(cv2.inRange(blurred, colorL, colorH), None, iterations=2), None, iterations=2)
    # Find contours of the mask and compute the fitting circle
    cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Only proceed if the ball was actually found
    if len(cnts) > 0:
        # Find the largest contour and fit a circle to it
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        return (x, y), radius
    else:
        return (0, 0), 0
