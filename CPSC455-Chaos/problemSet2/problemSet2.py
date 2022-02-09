from __future__ import division
import decimal
from sympy import *
from sympy import UnevaluatedExpr as uv
import numpy as np
import matplotlib.pyplot as plt
import pprint
import iterate

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
        fixed_points = iterate.find_fixed_points(expression)
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

    iterate.plot_graph_helper(graph_list,
                              f'F(x) = {expression}, x0 = {value}', "Iterations", "Value", f'Basin of attraction of F(x) = {expression}, seed = {value}', success, logarithm)
    return graph_list


def main():
    expr4 = sympify(x*((x**2) - 4))
    
    t = np.linspace(-3, 3, 100)
    values = t*((t**2) - 4)
    fig, ax = plt.subplots()
    ax.plot(t, values)
    ax.grid()
    
    plt.text(.3, -.25,
                 f'Blue values converge to 0\nRed values converge to 2\nGreen values converge to -2', transform=ax.transAxes)
    
    for item in np.linspace(-3, 3, 100):
        success, graph_list = find_basin_of_attraction(expr4, item, 10)
        if graph_list[-1] == 2:
            ax.scatter(item, 0, color='tab:red')
        elif graph_list[-1] == -2:
            ax.scatter(item, 0, color='tab:green')
        elif graph_list[-1] == 0:
            ax.scatter(item, 0, color='tab:blue')
    
    
    
    

if __name__ == '__main__':
    main()
