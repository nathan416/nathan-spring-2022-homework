"""iterate functions
    By: Nathan Flack
    Version: 1.0
"""
from __future__ import division
import decimal
from sympy import *
from sympy import UnevaluatedExpr as uv
import numpy as np
import matplotlib.pyplot as plt
import pprint

SEED = 100

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def find_fixed_points(expression):
    return solve(Eq(expression, x), x)


def iterate_expression(expression, value, range_amount):
    """iterates over a function with the initial value and returns 
        the list of iterated values

    Args:
        expression (SymPy object)): function of x to be iterated
        value (float): initial value
        range_amount (int): amount of iterations

    Returns:
        boolean: whether it was succcessful
        list: list of iterated values
    """
    result = expression.subs(x, value)
    iterate_list = [value, result]
    for loop_controller in range(0, range_amount):
        result = expression.subs(x, result)
        if result < 1e200 and result > -1e200:
            iterate_list.append(result)
        else:
            break
    return True, iterate_list


def calculate_square(value, seed, precision):
    try:
        if value == 0:
            raise ZeroDivisionError
        success = True
        w = seed
        graph1 = []
        graph1.append(w)
        last_w = w + 1
        count = 0

        while round(last_w - w, precision + 1) != 0 and count < 100:
            if w == 0:
                raise ZeroDivisionError
            if count > 98:
                success = False
            last_w = w
            w = w - (w**2 - value)/(2*w)
            graph1.append(w)
            count += 1
        return success, graph1
    except ZeroDivisionError as err:
        print('F\'(x) is 0:', err)


def iterate_over_range(expression, max):
    iterate_dict = {}
    for item in np.arange(-1*max - 1, max + 1, .0001):
        success, iterate_list = iterate_expression(
            expression, item, 20)
        iterate_dict[item] = iterate_list[-1]
    return iterate_dict


def plot_graph_helper(graph_list, title, xlabel, ylabel, window_name, success=True, logarithm=False):
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    fig, ax = plt.subplots(num=window_name)
    if logarithm:
        plt.semilogy(range(0, len(graph_list)), graph_list)
    else:
        plt.plot(range(0, len(graph_list)), graph_list)
    plt.title(title, fontdict=font1)
    plt.xlabel(xlabel, fontdict=font2)
    plt.ylabel(ylabel, fontdict=font2)

    if success:
        plt.text(.3, .7,
                 f'      Last Value: {float(graph_list[-1])}\nSecond to Last: {float(graph_list[-2])}', transform=ax.transAxes)
    else:
        plt.text(int(len(graph_list)/2), 0.7*SEED, 'unable to calculate')


def plot_iterate_graph(precision, expression, value, range_amount, logarithm=False):
    """puts arguments into iterate() function then plots the resulting graph

    Args:
        precision (int): [description]
        expression (SymPy object): function of x to be iterated
        value (float): initial value
        range_amount (int): times that the function should be iterated
        logarithm (bool, optional): whether the y axis should be logarithmic. Defaults to False.

    Returns:
        list: graphed list
    """
    success, graph_list = iterate_expression(expression, value, range_amount)

    plot_graph_helper(graph_list,
                      f'F(x) = {expression}, x0 = {value}', "Iterations", "Value", f'Iteration of F(x) = {expression}, x0 = {value}', success, logarithm)
    return graph_list


def plot_square_graph(precision, value):
    success, graph_list = calculate_square(value, SEED, precision)
    plot_graph_helper(graph_list,
                      "Newton's Method", "Iterations", "Value", 'Square of ' + str(value) +
                      ' with precision of ' + str(precision))
    return graph_list


def main():
    pass


if __name__ == '__main__':
    main()
