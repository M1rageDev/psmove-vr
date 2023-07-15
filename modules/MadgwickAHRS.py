import glm

class MadgwickAHRS:
    def __init__(self, initialPose: glm.quat):
        self.q = initialPose

    def update(self, g, a, b, timestep):
        Quat = self.q
        q1 = Quat.w
        q2 = Quat.x
        q3 = Quat.y
        q4 = Quat.z

        _2q1 = 2.0 * q1
        _2q2 = 2.0 * q2
        _2q3 = 2.0 * q3
        _2q4 = 2.0 * q4
        _4q1 = 4.0 * q1
        _4q2 = 4.0 * q2
        _4q3 = 4.0 * q3
        _8q2 = 8.0 * q2
        _8q3 = 8.0 * q3
        q1q1 = q1 * q1
        q2q2 = q2 * q2
        q3q3 = q3 * q3
        q4q4 = q4 * q4

        # Normalise accelerometer measurement
        norm = glm.sqrt(a.x * a.x + a.y * a.y + a.z * a.z)
        if norm == 0.0: return  # handle NaN
        norm = 1 / norm  # use reciprocal for division
        a.x *= norm
        a.y *= norm
        a.z *= norm

        # Gradient decent algorithm corrective step
        s1 = _4q1 * q3q3 + _2q3 * a.x + _4q1 * q2q2 - _2q2 * a.y
        s2 = _4q2 * q4q4 - _2q4 * a.x + 4.0 * q1q1 * q2 - _2q1 * a.y - _4q2 + _8q2 * q2q2 + _8q2 * q3q3 + _4q2 * a.z
        s3 = 4.0 * q1q1 * q3 + _2q1 * a.x + _4q3 * q4q4 - _2q4 * a.y - _4q3 + _8q3 * q2q2 + _8q3 * q3q3 + _4q3 * a.z
        s4 = 4.0 * q2q2 * q4 - _2q2 * a.x + 4.0 * q3q3 * q4 - _2q3 * a.y
        norm = 1.0 / glm.sqrt(s1 * s1 + s2 * s2 + s3 * s3 + s4 * s4)  # normalise step magnitude
        s1 *= norm
        s2 *= norm
        s3 *= norm
        s4 *= norm

        # Compute rate of change of quaternion
        qDot1 = 0.5 * (-q2 * g.x - q3 * g.y - q4 * g.z) - b * s1
        qDot2 = 0.5 * (q1 * g.x + q3 * g.z - q4 * g.y) - b * s2
        qDot3 = 0.5 * (q1 * g.y - q2 * g.z + q4 * g.x) - b * s3
        qDot4 = 0.5 * (q1 * g.z + q2 * g.y - q3 * g.x) - b * s4

        # Integrate to yield quaternion
        q1 += qDot1 * timestep
        q2 += qDot2 * timestep
        q3 += qDot3 * timestep
        q4 += qDot4 * timestep
        norm = 1.0 / glm.sqrt(q1 * q1 + q2 * q2 + q3 * q3 + q4 * q4)  # normalise quaternion
        Quat.w = q1 * norm
        Quat.x = q2 * norm
        Quat.y = q3 * norm
        Quat.z = q4 * norm
