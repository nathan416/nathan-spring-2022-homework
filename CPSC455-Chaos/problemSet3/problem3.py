from __future__ import division
from decimal import Decimal as D
from sympy import *
from sympy import UnevaluatedExpr as uv
import numpy as np
import matplotlib.pyplot as plt
import pprint as pp
from iterate import *
import math
from scipy.optimize import fsolve, root
import time


x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def main():
    expression_e = Piecewise( (2*x, (x<1/2) & (x>=0)), (2*x - 1, (x<1) & (x>=1/2)) , (x, True))
    
    composed_expression_e = expression_e.subs(x, expression_e)
    derivative_of_composed_e = diff(composed_expression_e, x)
    pp.pp(expression_e)
    pp.pp(composed_expression_e)
    pp.pp(derivative_of_composed_e)
    pp.pp(derivative_of_composed_e.subs(x, .2))
    
    plt.show(block=True)
    

if __name__ == '__main__':
    main()
