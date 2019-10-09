"""This is the selfish mining attack simulation
"""
import random
#import math
import numpy as np
#################################################
def sm_formula(gamma, _q):
    """This returns the correct answer that formula predicts
    """
    return (_q*(1 - _q)**2*(4*_q + gamma*(1-2*_q)) - _q**3)/(1 - _q*(1 + (2 - _q)*_q))

def evaluate():
    """This compares the difference between the right answer and simulated answer
    """
    with open('hw3-results.csv', 'r') as fd_0:
        for line in fd_0.read().split('\n'):
            vals = line.split(",")
            if len(vals) < 3:
                break
            t_gamma = float(vals[0])
            t_q = float(vals[1])
            mean = np.mean([float(x) for x in vals[2:]])
            answer = sm_formula(t_gamma, t_q)
            correct = "Good" \
                  if len(vals[2:]) >= 100  and (answer - 0.005 < mean < answer + 0.005) else "Bad"
            print("%0.2f, %0.2f, %d, %0.3f, %0.3f: %s" % \
                  (t_gamma, t_q, len(vals[2:]), mean, answer, correct))
###################################################

def selfish_trial(gamma, _q):
    """This function simulates selfish mining attack
    """
    public_sum = 0
    private_sum = 0
    public_length = 0
    private_length = 0

    while public_sum < 1000:
        _b = random.random()
        if _b <= _q:
            diff = private_length - public_length
            private_length += 1
            if diff == 0 and private_length == 2:
                public_sum += 2
                private_sum += 2
                public_length = 0
                private_length = 0
        else:
            diff = private_length - public_length
            public_length += 1
            if diff == 0:
                public_sum += 1
                if private_length > 0:
                    breaker = random.random()
                    if breaker <= gamma:
                        private_sum += 1
                        public_sum += 1
                    else:
                        public_sum += 1
                public_length = 0
                private_length = 0
            elif diff == 2:
                public_sum += private_length
                private_sum += private_length
                public_length = 0
                private_length = 0

    return float(private_sum)/(public_sum)


def selfish_sim(gamma, _q):
    """This function returns the list of percentages of selfish mining blocks
    in each run"""
    props = [] # array of results, each a value between 0 and 1
    for i in range(0, 1000): # you need more than 5...
      #call selfish_trial() in here somewhere
        i = selfish_trial(gamma, _q)
        props.append(i)
    return props


with open('hw3-results.csv', 'w') as fd_1:
    for i_q in np.arange(.05, 0.5, .05):
        i_q = round(i_q, 2)
        for i_gamma in [1, .5, 0]:
            results = selfish_sim(i_gamma, i_q)
            fd_1.write("%0.2f, %0.2f, %s\n" %(i_gamma, i_q, ", ".join([str(x) for x in results])))

evaluate()
