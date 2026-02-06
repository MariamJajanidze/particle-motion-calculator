# this file defines time-dependent forces functions. we may add more forces later 

import math 
def constant_force(F):
    return lambda t: F 

def sinusoidal_force(F0, omega):
    return lambda  t: F0*math.sin(omega*t)

def linear_force(k):
    return lambda t: k*t

def exponential_force(F0, tau):
    return lambda t: F0*math.exp(-t/tau)
