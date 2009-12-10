from numpy import *

s = arange(257)/256.0

z = s[::-1]

# lookup table
b = transpose(array((z*z*z,
                   3*z*z*s,
                   3*z*s*s,
                     s*s*s)))

def cubicspline(c,t): return dot(b[t],c)


