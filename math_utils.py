import math

def restrictVal(val, e):
    return math.copysign(min(math.fabs(val), e),val)

def limitPositionMovement(desiredMovement, epsilon):
    assert(epsilon > 0)
    desiredMovement[0] = restrictVal(desiredMovement[0], epsilon)
    desiredMovement[1] = restrictVal(desiredMovement[1], epsilon)
    desiredMovement[2] = restrictVal(desiredMovement[2], epsilon)

    return desiredMovement

def getMovement(currPos, goalPos, currOrientation, max_movement):
    delta = goalPos - currPos
    delta = limitPositionMovement(delta, max_movement)
    output = [0,0,0,0,0,0]
    for i in range(6):
        if(i < 3):
            output[i] = currPos[i] + delta[i]
        else:
            output[i] = currOrientation[i - 3]
    return output

def printArray(arr):
    out = "["
    for i in arr:
        out += "{:.2f},".format(i)
    out += "]"
    return out