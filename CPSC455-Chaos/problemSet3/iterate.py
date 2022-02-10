"""iterate functions
    By: Nathan Flack
    Version: 1.2
"""
from __future__ import division
import decimal
from sympy import *
from sympy import UnevaluatedExpr as uv
import numpy as np
import matplotlib.pyplot as plt
import pprint as pp
import traceback
from decimal import Decimal as D

SEED = 100

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def find_fixed_points(expression):
    try:
        fixed_points = solve(Eq(expression, x), x)
    except NotImplementedError as exc:
        # print(traceback.format_exc())
        print(exc)
        return []
    return fixed_points


def iterate_expression(expression, value, precision, max_iterations=100000):
    """iterates over a function with the initial value and returns 
        the list of iterated values

    Args:
        expression (SymPy object)): function of x to be iterated
        value (float): initial value
        precision (int): decimal precision
        max_iterations (int): amount of iterations

    Returns:
        list: list of iterated values
    """
    iterating_value = expression.subs(x, value)
    last_iterating_value = iterating_value + 1
    iterate_list = [value, iterating_value]
    count = 0

    while abs(last_iterating_value - iterating_value) > 10**(-1*precision) and count < max_iterations:
        last_iterating_value = iterating_value
        iterating_value = round(expression.subs(x, iterating_value), 14)
        if iterating_value < 1e200 and iterating_value > -1e200:
            iterate_list.append(iterating_value)
        else:
            break
        count += 1
    return iterate_list


def lab_iterate_expression(expression, value, precision):
    """iterates over a function with the initial value and returns 
        the list of iterated values

    Args:
        expression (SymPy object)): function of x to be iterated
        value (float): initial value
        precision (int): amount of iterations

    Returns:
        list: list of iterated values
    """
    fixed_points = find_fixed_points(expression)
    result = expression.subs(x, value)
    iterate_list = [value, result]

    iterating_value = value
    last_iterating_value = iterating_value + 1
    count = 0

    while abs(last_iterating_value - iterating_value) > 10**(-1*precision) and iterating_value not in fixed_points and count < 100000:
        last_iterating_value = iterating_value
        iterating_value = expression.subs(x, iterating_value)
        if int(iterating_value) < 1e200 and int(iterating_value) > -1e200:
            iterate_list.append(iterating_value)
        else:
            break
        count += 1
    return iterate_list


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
        iterate_list = iterate_expression(
            expression, item, 20)
        iterate_dict[item] = iterate_list[-1]
    return iterate_dict


def plot_graph_helper(graph_list, title, xlabel, ylabel, window_name, is_logarithm=False, has_grid = False, success=True):
    """takes a list and plots it out. takes arguments that are used in displaying the graph

    Args:
        graph_list (list): list of numbers used as the y values in the graph
        title (string): [description]
        xlabel (string): [description]
        ylabel (string): [description]
        window_name (string): [description]
        is_logarithm (bool, optional): whether to use the log scale on the y graph. Defaults to False.
        has_grid (bool, optional): displays red grid lines. Defaults to False.
        success (bool, optional): [description]. Defaults to True.
    """
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    fig, ax = plt.subplots(num=window_name)
    
    if is_logarithm:
        ax.semilogy(range(0, len(graph_list)), graph_list)
    else:
        ax.plot(range(0, len(graph_list)), graph_list)
    
    plt.title(title, fontdict=font1)
    plt.xlabel(xlabel, fontdict=font2)
    plt.ylabel(ylabel, fontdict=font2)
    if has_grid:
        ax.grid(color='r', linestyle='-', linewidth=.5)

    if success:
        ax.text(.3, .7,
                 f'      Last Value: {float(graph_list[-1])}\nSecond to Last: {float(graph_list[-2])}', transform=ax.transAxes)
    else:
        ax.text(int(len(graph_list)/2), 0.7*SEED, 'unable to calculate')


def plot_iterate_graph(precision, expression, value, is_logarithm=False, max_iterations=100000, has_grid=False):
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
    graph_list = iterate_expression(
        expression, value, precision, max_iterations)

    plot_graph_helper(graph_list,
                      f'F(x) = {expression}, x0 = {value}', "Iterations", "Value", f'Iteration of F(x) = {expression}, x0 = {value}', is_logarithm, has_grid)
    return graph_list


def plot_square_graph(precision, value):
    success, graph_list = calculate_square(value, SEED, precision)
    plot_graph_helper(graph_list,
                      "Newton's Method", "Iterations", "Value", 'Square of ' + str(value) +
                      ' with precision of ' + str(precision))
    return graph_list


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
        return graph1
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


def main():
    pass


if __name__ == '__main__':
    main()
