import math

def generateCirclePoints(xc, yc, r, N):
    xpts = []
    ypts = []
    for i in range(N+1):
        theta = (float(i)/N)*2*math.pi
        #print theta
        xpoint = xc + r*math.sin(theta)
        ypoint = yc + r*math.cos(theta)
        xpts.append(xpoint)
        ypts.append(ypoint)
    return xpts, ypts

def generateCirclePointsZip(xc, yc, r, N):
    points = []
    for i in range(N+1):
        theta = (float(i)/N)*2*math.pi
        #print theta
        xpoint = xc + r*math.sin(theta)
        ypoint = yc + r*math.cos(theta)
        points.append([xpoint,ypoint])
    return [points]
