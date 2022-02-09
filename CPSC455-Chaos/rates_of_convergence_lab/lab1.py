from __future__ import division
import decimal
from sympy import *
from sympy import UnevaluatedExpr as uv
import numpy as np
import matplotlib.pyplot as plt
import pprint as pp
from iterate import *
import math
from scipy.optimize import fsolve, root
import time

SEED = 100

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def find_basin_of_attraction(expression, seed, precision):
    """finds the basin of attraction

    Args:
        expression (SymPy object): [description]
        seed (float): seed value
        precision (int): decimal precision

    Returns:
        list: list of iterated values
    """
    try:
        fixed_points = find_fixed_points(expression)
        derivative = diff(expression, x)
        if seed == 0:
            raise ZeroDivisionError
        success = True
        w = seed
        graph1 = []
        graph1.append(w)
        last_w = w + 1
        count = 0

        while round(last_w - w, precision + 1) != 0 and count < 100:
            if derivative.subs(x, w) == 0:
                raise ZeroDivisionError
            if count > 98:
                success = False
            last_w = w
            w = w - (expression.subs(x, w))/(derivative.subs(x, w))
            graph1.append(w)
            count += 1
        return success, graph1
    except ZeroDivisionError as err:
        print('F\'(x) is 0:', err)


def plot_basin_graph(precision, expression, value, logarithm=False):
    """puts arguments into find_basin_of_attraction() function then plots the resulting graph

    Args:
        precision (int): [description]
        expression (SymPy object): function of x
        value (float): seed value
        logarithm (bool, optional): whether the y axis should be logarithmic. Defaults to False.

    Returns:
        boolean: success
        list: graphed list
    """
    success, graph_list = find_basin_of_attraction(
        expression, value, precision)

    plot_graph_helper(graph_list,
                              f'F(x) = {expression}, x0 = {value}', "Iterations", "Value", f'Basin of attraction of F(x) = {expression}, seed = {value}', success, logarithm)
    return graph_list


def function_k(k):
    return [np.sin(k[0])]


def main():
    INITIAL_VALUE = 0.2
    PRECISION = 8
    
    expression_a = sympify((x**2) + .25)
    expression_b = sympify(x**2)
    expression_c = sympify((x**2) - .24)
    expression_d = sympify((x**2) - .75)
    expression_e = sympify(.4*x*(1-x))
    expression_f = sympify(x*(1-x))
    expression_g = sympify(1.6*x*(1-x))
    expression_h = sympify(2*x*(1-x))
    expression_i = sympify(2.4*x*(1-x))
    expression_j = sympify(3*x*(1-x))
    expression_k = sympify(0.4*sin(x))
    expression_l = sympify(sin(x))
    
    # expression_m = atan(x)
    # plot_iterate_graph(8, expression_m, .1)
    
    # plt.show(block=True)
    
    
    result_a = lab_iterate_expression(expression_a, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_a):<13}: {len(result_a):^10}, Number converged on: {result_a[-1]}')
    result_b = lab_iterate_expression(expression_b, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_b):<13}: {len(result_b):^10}, Number converged on: {result_b[-1]}')
    result_c = lab_iterate_expression(expression_c, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_c):<13}: {len(result_c):^10}, Number converged on: {result_c[-1]}')
    result_d = lab_iterate_expression(expression_d, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_d):<13}: {len(result_d):^10}, Number converged on: {result_d[-1]}')
    result_e = lab_iterate_expression(expression_e, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_e):<13}: {len(result_e):^10}, Number converged on: {result_e[-1]}')
    result_f = lab_iterate_expression(expression_f, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_f):<13}: {len(result_f):^10}, Number converged on: {result_f[-1]}')
    result_g = lab_iterate_expression(expression_g, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_g):<13}: {len(result_g):^10}, Number converged on: {result_g[-1]}')
    result_h = lab_iterate_expression(expression_h, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_h):<13}: {len(result_h):^10}, Number converged on: {result_h[-1]}')
    result_i = lab_iterate_expression(expression_i, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_i):<13}: {len(result_i):^10}, Number converged on: {result_i[-1]}')
    result_j = lab_iterate_expression(expression_j, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_j):<13}: {len(result_j):^10}, Number converged on: {result_j[-1]}')
    result_k = lab_iterate_expression(expression_k, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_k):<13}: {len(result_k):^10}, Number converged on: {result_k[-1]}')
    result_l = lab_iterate_expression(expression_l, INITIAL_VALUE, PRECISION)
    print(f'Number of Iterations for {str(expression_l):<13}: {len(result_l):^10}, Number converged on: {result_l[-1]}')
    
    
    
if __name__ == '__main__':
    main()
