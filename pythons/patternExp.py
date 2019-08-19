import pythons.check as ch
import json
import os 
import numpy as np

def loadJson(_route):
    fileList = [f for f in os.listdir(_route) if os.path.isfile(_route + f)]
    jsons = dict()
    for i, r in enumerate(fileList):
        js = json.load(open(_route + r))
        print(r)
        jsons[r] = js
    return jsons

def exp(_js, _ans):
    keys = _js.keys()
    ret = []
    ch.loadAnswer(_ans)
    count = 0
    for i, e in enumerate(keys):
        env = e.split('-')[1][0:2]
        tmp = np.append(np.array(e), np.array(ch.check(_js[e])))
        tmp = np.append(env, tmp)
        ret.append(tmp)
        if env == _ans:
            count += 1
    return np.array(ret), count

def classify(r, env):
    a = r.transpose()
    ret = dict()
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    for i, e in enumerate(a[0]):
        if (env == e):
            if (a[2][i] == '0'):
                TP = TP + 1
            elif (a[2][i] == '-1'):
                FN = FN + 1
        elif (env != e):
            if (a[2][i] == '0'):
                FP = FP + 1
            elif (a[2][i] == '-1'):
                TN = TN + 1
    return TP, FP, TN, FN



# 정답이냐 아니냐를 따지는 실험도 있겠지만 아예 classification 성능을 실험해보는 것도 좋을듯.
# 결과가 아무 환경과도 같지 않다고 할 때 어떤 의미가 있나? 결국 binary classify 이상의 의미를 끌어내기는 힘들듯.
js = loadJson('exp/dataPattern/')

ret = []
def ban():
    envs = ['10', '20', '30', '40', '50']
    for i, env in enumerate(envs):
        r, count = exp(js, env)
        # print("env: " + env + ", number:" + str(count))
        # print("TP, FP, TN, FN")
        # print()
        c = classify(r, env)
        print(env + ", " + str(count) + ", " + str(c[0]) + ", " + str(c[1]) + ", " + str(c[2]) + ", " + str(c[3]))
# for i, j in enumerate(js[1]):
#     env = e.split('-')[1][0:2]
#     print('env: ' + env)
#     ret.append(())

ds = [50, 60, 70, 80, 90, 100, 110, 120]
ts = [0.1, 0.2, 0.3]

for i, t in enumerate(ts):
    for j, d in enumerate(ds):
        ch.setParam(d, t)
        print(str(d) + ", " + str(t))
        ban()
        