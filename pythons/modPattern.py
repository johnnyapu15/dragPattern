import os
import json

def loadJson(_route):
    fileList = [f for f in os.listdir(_route) if os.path.isfile(_route + f)]
    jsons = dict()
    keys = []
    for i, r in enumerate(fileList):
        js = json.load(open(_route + r))
        print(r)
        jsons[r] = js
        keys.append(r)
    return jsons, keys


js = loadJson('exp/dataPattern/')


for i, e in enumerate(js[1]):
    env = e.split('-')[1][0:2]
    js[0][e]


