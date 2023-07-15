from math import sqrt

def estimatePos(x, y, distance, focalX, fShape):
    x_px = x - fShape[1] / 2
    y_px = fShape[0] / 2 - y

    L_px = sqrt(x_px * x_px + y_px * y_px)
    k = L_px / focalX  # focal length x
    z_cm = distance

    L_cm = z_cm * k
    x_cm = L_cm * x_px / L_px
    y_cm = L_cm * y_px / L_px

    return x_cm, y_cm, z_cm
