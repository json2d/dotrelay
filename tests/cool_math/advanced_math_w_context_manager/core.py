import os

import dotrelay

with dotrelay.Radio(__file__):
  from basic_math import mult

def sqr(a):
  return mult(a,a)