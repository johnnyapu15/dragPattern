import json
import math

r = 100 # px
t = 0.1 # rad
ans = json.load(open("./exp/answer/test.json", 'r'))
route = "./exp/answer/"
def getDistance(_pnt1, _pnt2):
    return math.sqrt(math.pow((_pnt1[0] - _pnt2[0]),2) + math.pow((_pnt1[1] - _pnt2[1]), 2))

def loadAnswer(_ans = "test"):
    global ans, route
    ans = json.load(open(route + _ans + ".json", 'r'))

def setParam(_r, _t):
    global r, t
    r = _r
    t = _t
    #print("Setting exp params... " + str(_r) + ", " + str(_t))

def check(_ret):
    global ans, route, r, t
    for i, e in enumerate(ans.keys()):
        # print(" --- " + str(ans[e]))
        # print(" --- " + str(_ret[e]))
        if (e not in _ret.keys()):
            return -1, "CANT FIND DEVICE"
        else:
            dis = getDistance(ans[e][0][0], _ret[e][0][0])
            if dis > r:
                return -1, "WRONG PATTERN: R" + e
            else:
                # Check theta
                if abs(_ret[e][2] - ans[e][2]) > t * 2:
                    return -1, "WRONG PATTERN: T" + e
                else:
                    continue#print("Checked ... " + e)
    return 0, "Good"

            



# test = json.load(open("./exp/answer/test.json", 'r'))
# check(test)