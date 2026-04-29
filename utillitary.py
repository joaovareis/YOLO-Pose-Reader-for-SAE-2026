import math

#We use custom definitions for dot and cross prod since YOLO Y axis is inverted and we only have two axis
def calc_vector (kp1, kp2):

    v_x = kp2[0] - kp1[0]
    v_y = -kp2[1] + kp1[1]

    return [v_x, v_y]

def dot_prod (v1, v2):

    dp = v1[0]*v2[0] + v1[1]*v2[1]

    return dp

def cross_prod (v1, v2):

    cp = (v1[0]*v2[1]) - (v1[1]*v2[0])

    return cp

def calc_angle(v1, v2):
    #In order to find the angle between the base and needle vectors, we use atan2 with the cross and dot products
    #By definition, this cancels out the vector norm, leaving only the ratio between sin and cos. Which atan2 returns a unique value for all quadrants

    dot = dot_prod(v1, v2)
    cross = cross_prod(v1, v2)

    rad = math.atan2(cross, dot)
    deg = rad*(180/math.pi)

    return deg

def interpolate (deg):
    #Atan2 will return a value starting from -30° -> 0 to -180° -> 50, then from 180° -> 50 to 30° -> 100
    if deg < 0:

        read = -deg*1/3 - 10

    else:

        read = -deg*1/3 + 110

    return read
