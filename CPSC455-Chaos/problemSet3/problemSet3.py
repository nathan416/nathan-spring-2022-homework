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
    INITIAL_VALUE = 0.2
    PRECISION = 8

    expression_a = sympify((x**2) + .25)
    expression_b = atan(x)
    expression_c = Piecewise( (2*x, x<=1/2), (2 - 2*x, x>1/2) )
    expression_d = sympify((-1/2 * x**3) - (3/2 * x**2) + 1)
    expression_e = Piecewise( (2*x, (x<1/2) & (x>=0)), (2*x - 1, (x<1) & (x>=1/2)) )
    
    # plot_iterate_graph(8, expression_b, .3, max_iterations=1000)
    # plot_iterate_graph(8, expression_c, .2, max_iterations=10)
    graph_list_e = plot_iterate_graph(8, expression_e, D(.6), max_iterations=1000, has_grid=True)
    pp.pp(graph_list_e)
    plt.show(block=True)
    
    # -1.00000000000000
    # 0.732050807568877
    # -2.73205080756888
    
    # t = np.linspace(-4, 2, 100)
    # values = (-1/2 * t**3) - (3/2 * t**2) + 1
    # fig, ax = plt.subplots()
    # ax.plot(t, values)
    # ax.grid()
    
    # plt.text(.3, -.25,
    #              f'Blue values converge to 0\nRed values converge to 2\nGreen values converge to -2', transform=ax.transAxes)
    
    # for item in np.linspace(-4, 2, 101):
    #     graph_list = find_basin_of_attraction(expression_d, item, 10)
        
    #     if graph_list[-1] < -2:
    #         ax.scatter(item, 0, color='tab:red')
    #     elif graph_list[-1] > 0:
    #         ax.scatter(item, 0, color='tab:green')
    #     else:
    #         ax.scatter(item, 0, color='tab:blue')
        
    # plt.show(block=True)


if __name__ == '__main__':
    main()
