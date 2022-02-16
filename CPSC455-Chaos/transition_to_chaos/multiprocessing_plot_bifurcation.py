from __future__ import division

import psutil
import decimal
from functools import partial
import itertools
import math
import multiprocessing
import pprint as pp
import time
from itertools import repeat

import matplotlib.pyplot as plt
import numpy as np
from click import progressbar
from scipy.optimize import fsolve, root
from sympy import UnevaluatedExpr as uv
from sympy import *
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map, process_map

from iterate import *

SEED = 100

x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def plot_bifurcation_graph(expression, initial_value=0.0, max_iterations=80, minimum_c=-2, maximum_c=-.4, print_progressbar=False, samples=250):
    time_start = time.perf_counter()
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}
    fig, ax = plt.subplots(
        num=f'Bifurcation plot of F(x) = {expression}, between {minimum_c} and {maximum_c}')
    plt.title(
        f'F(x) = {expression}, between {minimum_c} and {maximum_c}', fontdict=font1)
    plt.xlabel('y', fontdict=font2)
    plt.ylabel('x', fontdict=font2)
    # plt.ylim(-2, 2)

    x_array = []
    y_array = []
    
    x_y_array = process_map(partial(map_bifurcation_helper, expression=expression, initial_value=initial_value, max_iterations=max_iterations), np.linspace(
        minimum_c, maximum_c, samples), max_workers=psutil.cpu_count(logical=False), chunksize=2)
    
    x_y_array = list(itertools.chain.from_iterable(x_y_array))
    
    for x_y in x_y_array:
        x_array.append(x_y[0])
        y_array.append(x_y[1])
    ax.scatter(x_array, y_array, s=.1)

def map_bifurcation_helper(c_value, expression, initial_value, max_iterations):
    x_y_array = []

    expr_c = expression.subs(y, c_value)
    graph_list = iterate_expression(
        expr_c, initial_value, 8, max_iterations)

    if len(graph_list) > 50:
        for iterated_value in graph_list[50:]:
            x_y_array.append((c_value, iterated_value))
    elif len(graph_list) > 15:
        for iterated_value in graph_list[15:]:
            x_y_array.append((c_value, iterated_value))
    else:
        for iterated_value in graph_list[2:]:
            x_y_array.append((c_value, iterated_value))
    return x_y_array

def main():
    expr4 = sympify((x**2) + y)
    expr_a = sympify(y*x*(1-x))
    plot_bifurcation_graph(expr_a, print_progressbar=True,
                           samples=1000, max_iterations=1000, minimum_c=-2, maximum_c=4, initial_value=.1)

    manager = plt.get_current_fig_manager()
    # manager.full_screen_toggle()

    plt.tight_layout()
    plt.show(block=true)


if __name__ == '__main__':
    main()
