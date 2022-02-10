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
    expression = sympify((x**3)/6 + x)
    derivative1 = diff(expression)
    derivative2 = diff(derivative1)
    derivative3 = diff(derivative2)
    
    pp.pp(f'F(x) = {str(expression):<19}, F(0) = {expression.subs(x, 0)}')
    pp.pp(f'F\'(x) = {str(derivative1):<18}, F\'(0) = {derivative1.subs(x, 0)}')
    pp.pp(f'F\'\'(x) = {str(derivative2):<17}, F\'\'(0) = {derivative2.subs(x, 0)}')
    pp.pp(f'F\'\'\'(x) = {str(derivative3):<16}, F\'\'\'(0) = {derivative3.subs(x, 0)}')
    
    plot_iterate_graph(8, expression, .1, max_iterations=300, has_grid=True)
    plot_iterate_graph(8, expression, -.1, max_iterations=300, has_grid=True)
        
    plt.show(block=True)
    

if __name__ == '__main__':
    main()
