from __future__ import division
import decimal
from sympy import *
import numpy as np
import matplotlib.pyplot as plt

SEED = 100

y, z, t = symbols('y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)


def calculate_square(value, seed, precision):
    try:
        if value == 0:
            raise ZeroDivisionError
        success = True
        x = seed
        graph1 = []
        graph1.append(x)
        last_x = x + 1
        count = 0
        
        while round(last_x - x, precision + 1) != 0 and count < 100:
            if x == 0:
                raise ZeroDivisionError
            if count > 98:
                success = False
            last_x = x
            x = x - (x**2 - value)/(2*x)
            graph1.append(x)
            count += 1
        return success, graph1
    except ZeroDivisionError as err:
        print('F\'(x) is 0:', err)

def plot_graph_helper(graph_list, precision, value, success):
    font1 = {'family':'serif','color':'blue','size':20}
    font2 = {'family':'serif','color':'darkred','size':15}
    plt.figure(num='Square of ' + str(value) + ' with precision of ' + str(precision))
    plt.plot(range(0, len(graph_list)), graph_list)
    plt.title("Newton's Method", fontdict = font1)
    plt.xlabel("Iterations", fontdict = font2)
    plt.ylabel("Value", fontdict = font2)
    if success:
        plt.text(int(len(graph_list)/2), 0.7*SEED, float(graph_list[-1]))
    else:
        plt.text(int(len(graph_list)/2), 0.7*SEED, 'unable to calculate')
        
    
def plot_graph(precision, value):
    success, graph_list = calculate_square(value, SEED, precision)
    plot_graph_helper(graph_list, precision, value, success)

    
def main():
       plot_graph(5, 11)
       plot_graph(10, 11)
       plot_graph(20, 11)
       plot_graph(20, -1)
       
       plt.show(block=True)

if __name__ == '__main__':
    main()