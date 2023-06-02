# Importing libraries
from fastapi import HTTPException
from scipy.optimize import linprog, OptimizeResult
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns

sns.set()

# Defining global variables
optimals_solution = []

# Function that solves the problem using the simplex method


def solve(c, A_ub, b_ub, A_eq, b_eq):
    # Defining the method to use
    method = 'simplex'
    global optimals_solution
    optimals_solution = []
    # Solving a problem with only unequalities
    if A_eq == [] and b_eq == []:
        result = linprog(c=c, A_ub=A_ub, b_ub=b_ub, method=method,
                         callback=print_optimal_solution_each_iteration)

    # Solving a problem with only equalities
    elif A_ub == [] and b_ub == []:
        result = linprog(c=c, A_eq=A_eq, b_eq=b_eq, method=method,
                         callback=print_optimal_solution_each_iteration)

    # Solving a problem with both equalities and inequalities
    else:
        result = linprog(c=c, A_ub=A_ub, b_ub=b_ub,
                         A_eq=A_eq, b_eq=b_eq, method=method,
                         callback=print_optimal_solution_each_iteration)

    # Printing the solution if it was found
    if result.success:
        # Graphing the solution if it is 2D
        optimals_solution = [list(x) for x in optimals_solution]

        if len(c) == 2:
            graph_lines(A_ub, b_ub, A_eq, b_eq)
            graph_path()
            plt.show()

        # Returning the optimal solution
        return optimals_solution

    # Returning an error if the solution was not found
    raise HTTPException(
        status_code=404, detail="Optimization failed. Check your constraints.")


def print_optimal_solution_each_iteration(data: OptimizeResult):
    if len(data.x) == 2:
        plt.scatter(data.x[0], data.x[1])

    global optimals_solution
    optimals_solution.append(data.x)


def graph_path():
    global optimals_solution

    for i in range(len(optimals_solution)-1):
        xs = [optimals_solution[i][0], optimals_solution[i+1][0]]
        ys = [optimals_solution[i][1], optimals_solution[i+1][1]]
        plt.plot(xs, ys, linestyle="--", color='red')

        # Mostramos en la gráfica a qué punto se refiere cada coordenada
        plt.text(xs[0]-0.015, ys[0]+0.25, "Point" + str(i))
        plt.text(ys[1]-0.015, ys[1]+0.25, "Point" + str(i))


def graph_lines(A_ub, b_ub, A_eq, b_eq, max_x=5, max_y=10):
    Ys = []
    for fila, b in zip(A_ub, b_ub):
        if fila[1] != 0:
            X = np.linspace(0, max_x, 10000)
            Y = recta(fila[0], fila[1], b, X)
            if np.all((Y == np.zeros(10000)) == True):
                pass
            else:
                Ys.append(Y)
        else:
            X = np.array([fila[1]] * 10000)
            Y = np.linspace(0, max_y, 10000)

        # plt.fill_between(X, Y, 0, where=(X>0) & (X<=5), color='red')
        plt.plot(X, Y, color='blue')

    for fila, b in zip(A_eq, b_eq):
        if fila[1] != 0:
            X = np.linspace(0, max_x, 10000)
            Y = recta(fila[0], fila[1], b, X)
            if np.all((Y == np.zeros(10000)) == True):
                pass
            else:
                Ys.append(Y)
        else:
            X = np.array([fila[1]] * 10000)
            Y = np.linspace(0, max_y, 10000)

        # plt.fill_between(X, Y, 0, where=(X>=0) & (X<=5), color='red')
        plt.plot(X, Y, color='red')

    Ys = np.array(Ys)
    mins = np.min(Ys, axis=0)
    mins = mins[mins >= 0]

    X = np.linspace(0, 5, 10000)
    X = X[:len(mins)]
    plt.fill_between(X, mins, 0, where=(X >= 0) & (X <= 5), color='yellow')
    # plt.show()


def recta(a, b, c, x):
    return (c - a * x) / b
