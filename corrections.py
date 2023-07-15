def correctBallOffset(rp, rq, up, chl):  # real position, real quaternion, up direction, controller half length
    rd = up * rq
    return rp - rd * chl

def headOffsetCorrection(rp, ho):  # real position, head offset
    return rp - ho
