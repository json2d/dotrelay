import os

import dotrelay
dotrelay.init(__file__)

from basic_math import mult

def sqr(a):
  return mult(a,a)