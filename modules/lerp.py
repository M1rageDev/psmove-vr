import glm

def lerp(a, b, u):
    return a*(1. - u) + b*u

def clamp(x, l, h):
    return min(max(x, l), h)

def clamp01(x):
    return clamp(x, 0., 1.)

def posFilter(l, c):
    lv = glm.vec3(l[0], l[1], l[2])
    cv = glm.vec3(c[0], c[1], c[2])
    distance = glm.length(lv - cv)
    XYweight = clamp01(lerp(0.4, 1.0, distance / 5.0))
    Zweight = clamp01(lerp(0.2, 1.0, distance / 5.0))

    x = lerp(lv.x, cv.x, XYweight)
    y = lerp(lv.y, cv.y, XYweight)
    z = lerp(lv.z, cv.z, Zweight)

    return glm.vec3(x, y, z)
