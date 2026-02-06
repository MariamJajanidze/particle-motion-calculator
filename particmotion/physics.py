#handling all the physics: classical and relativistic mechanics for motion and time-dependent forces 


import math
c=299792458 #the speed of light
def classical_motion(m,v0,force_func, t):
    dt=t / 1000    #very small time step 
    v=v0
    for i in range(1000):
        F=force_func(i*dt)  #force formula for classical motion
        a=F / m             #acceleration formula for classical motion
        v+=a*dt
    p=m*v  #impulse formula for linear momentum
    return v,p

def relativistic_motion(m, v0, force_func, t):
    dt=t / 2000  # in relativistic mode we take even smaller time step 
    p=relativistic_p(m, v0)
    for i in range(2000):
        F=force_func(i*dt)
        p+=F*dt 
    v=relativistic_v(m, p)
    return v,p

def relativistic_p(m,v):
    gamma=1/math.sqrt(1-(v**2/c**2))
    return gamma*m*v

def relativistic_v(m,p):
    #solve v=p/sqrt.(m**2+(p**2/c**2))
    return p/math.sqrt(m**2+(p**2/c**2))
