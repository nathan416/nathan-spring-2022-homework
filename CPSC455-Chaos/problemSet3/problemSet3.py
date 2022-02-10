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


def graph_cobweb(expression, initial_value, max_iterations, low_range, high_range):
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    graph_list = iterate_expression(
        expression, initial_value, 8, max_iterations)
    t = np.linspace(low_range, high_range, 100)
    values = list(map(lambda j: expression.subs(x, j), t))
    fig, ax = plt.subplots(num=f'Cobweb plot of F(x) = {expression}, x0 = {initial_value}')
    plt.title(f'F(x) = {expression}, x0 = {initial_value}', fontdict=font2)
    plt.xlabel('x', fontdict=font2)
    plt.ylabel('y', fontdict=font2)
    ax.plot(t, values)
    ax.plot(t, t)
    ax.plot([initial_value, initial_value], [
            initial_value, graph_list[1]], color='r')
    ax.plot([initial_value, graph_list[1]], [
            graph_list[1], graph_list[1]], color='r')
    for loop_controller in range(1, len(graph_list) - 1):
        ax.plot([graph_list[loop_controller], graph_list[loop_controller]], [
                graph_list[loop_controller], graph_list[loop_controller + 1]], color='r')
        ax.plot([graph_list[loop_controller], graph_list[loop_controller + 1]],
                [graph_list[loop_controller + 1], graph_list[loop_controller + 1]], color='r')


def main():
    expression_a = Piecewise( (2*x, (x<1/2) & (x>=0)), (2*x - 1, (x<1) & (x>=1/2)) , (x, True))
    expression_b = sympify((x**3)/6 + x)
    expression_c = 2.8*x*(1-x)
    expression_d = atan(x)

    graph_cobweb(expression_a, .1, 20, 0, 1)
    graph_cobweb(expression_a, .111, 50, 0, 1)
    
    graph_cobweb(expression_b, .11, 247, -1, 1)
    graph_cobweb(expression_b, -1, 3, -3, 1)
    
    graph_cobweb(expression_c, .1, 20, 0, .65)
    graph_cobweb(expression_c, .9, 20, 0, 1)
    
    graph_cobweb(expression_d, 1, 50, -1, 1)
    graph_cobweb(expression_d, 2, 50, -1, 2)
    plt.show(block=True)


if __name__ == '__main__':
    main()
