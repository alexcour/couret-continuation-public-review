#!/usr/bin/env python3
import math

def triple_weight(l):
    probs={1:1/l**2,2:3*(l-1)/l**2,3:(l-1)*(l-2)/l**2}
    logs={nu:math.log((1-nu/l)/(1-1/l)**3) for nu in (1,2,3)}
    mu=sum(probs[nu]*logs[nu] for nu in probs)
    return sum(probs[nu]*(logs[nu]-mu)**2 for nu in probs)

for l in (7,11,13,17,19,23):
    print(l, triple_weight(l))
