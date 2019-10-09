"""This is the double spend attack simulation
"""

import random
import json
#import numpy as np
#from collections import defaultdict

def sim(q_sim, z_sim):
    """ This is the function where the simulated double spend attack happens
    """
    a_z = 0
    h_z = 0
    while (h_z - a_z) < 35:
        raw_num = random.randint(0, 101)
        q_num = raw_num / 100
        if q_num <= q_sim:
            a_z += 1
        else:
            h_z += 1
        if h_z >= z_sim:
            if a_z > h_z:
                return True
    return False

RESULTS = dict()
for run in range(2000001):
    rq = 0 + 0.01 * (int(run / 40001))
    rz = 1 + int((run % 40001)/801)
    q_index = int(rq * 100)
    if (q_index, rz) in RESULTS:
        RESULTS[(q_index, rz)] = RESULTS[(q_index, rz)] + sim(rq, rz)
    else:
        RESULTS[(q_index, rz)] = sim(rq, rz)

for key in RESULTS:
    RESULTS[key] = RESULTS[key] / 800

JSON_STR = open('test.json', 'r').read()
TESTS = json.loads(JSON_STR)

with open('results.csv', 'w') as fd:
    for x in TESTS:
        oq = x['q']
        phi = x['phi']
        oz = 0
        for i in range(1, 51):
            if phi == RESULTS[(int(oq*100), i)]:
                oz = i
            elif(phi > RESULTS[int(oq*100), i]) and (RESULTS[int(oq*100), i] > oz):
                oz = i
        if oz == 0:
            oz = -1
        print("q:\t%.2f\tPhi:%f\tz:%2d" % (oq, phi, oz))
        fd.write("q:\t%.2f\tPhi:%f\tz:%2d" % (oq, phi, oz))
