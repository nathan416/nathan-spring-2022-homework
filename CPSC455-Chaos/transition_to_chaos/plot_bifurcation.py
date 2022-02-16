from __future__ import division

import decimal
import math
import pprint as pp
import time

import matplotlib.pyplot as plt
import numpy as np
from click import progressbar
from scipy.optimize import fsolve, root
from sympy import UnevaluatedExpr as uv
from sympy import *

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

    def helper(bar):
        for c_value in bar:
            expr_c = expression.subs(y, c_value)
            graph_list = iterate_expression(
                expr_c, initial_value, 8, max_iterations)

            if len(graph_list) > 50:
                for iterated_value in graph_list[50:]:
                    x_array.append(c_value)
                    y_array.append(iterated_value)
            elif len(graph_list) > 15:
                for iterated_value in graph_list[15:]:
                    x_array.append(c_value)
                    y_array.append(iterated_value)
            else:
                for iterated_value in graph_list[2:]:
                    x_array.append(c_value)
                    y_array.append(iterated_value)

    if(print_progressbar):
        with progressbar(np.linspace(minimum_c, maximum_c, samples), fill_char='█', width=80, item_show_func=lambda x: f'x = {x} : time passed: {time.strftime("%H:%M:%S", time.gmtime(time.perf_counter() - time_start))}') as bar:
            helper(bar)
    else:
        helper(np.linspace(minimum_c, maximum_c, samples))

    ax.scatter(x_array, y_array, s=.1)


def main():
    expr4 = sympify((x**2) + y)
    plot_bifurcation_graph(expr4, print_progressbar=True,
                           samples=800, max_iterations=600, minimum_c=-2, maximum_c=.25)

    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    plt.tight_layout()
    plt.show(block=true)


if __name__ == '__main__':
    main()
