import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import tkinter as tk
from tkinter import Entry, Button, Label
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

entry_fields = []  # Define entry_fields only once

# Constants and colors
N = 15
EPSILON = 1e-8
STEP = 0.04
WINDOW = 2
colors = ["red", "blue", "yellow", "green", "magenta", "brown"]

# Function to update the constants
def update_constants():
    global N, EPSILON, STEP
    N = int(entry_n.get())
    EPSILON = float(entry_epsilon.get())
    STEP = float(entry_step.get())

def plot_polynomial_graph():
    polynomial_numbers = [int(entry_fields[i].get()) for i in range(7)]
    clean_polynomial_numbers = eraseLeadingZeros(polynomial_numbers)

    update_constants()  # Update constants from input fields

    x_points, y_points, convergence_points = findFunctionZeroes(
        EPSILON, N, STEP, WINDOW, clean_polynomial_numbers)

    color_array = getColorArrayForScatterPlot(x_points, y_points, convergence_points)

    np_x_points = np.array(x_points)
    np_y_points = np.array(y_points)

    scatter_plot.set_offsets(np.column_stack((np_x_points, np_y_points)))
    scatter_plot.set_array(np.array(color_array))
    ax.relim()
    ax.autoscale_view()
    

def eraseLeadingZeros(polynomialNumbers):
    for index in range(7):
        if polynomialNumbers[index] != 0:
            return polynomialNumbers[index:7]


def printFormula(PolynomialNumbers):
    formulaString = ""
    power = len(PolynomialNumbers) - 1
    for number in PolynomialNumbers[:len(PolynomialNumbers) - 1]:
        formulaString += f"{number}x^{power} + "
        power -= 1
    formulaString += f"{PolynomialNumbers[-1]}"
    print("The formula:")
    print(formulaString)


def function(PolynomialNumbers, x):
    result = 0.0
    power = len(PolynomialNumbers) - 1
    for number in PolynomialNumbers[:len(PolynomialNumbers) - 1]:
        result += number * x**power
        power -= 1
    result += PolynomialNumbers[-1]
    return result


def functionDerivative(PolynomialNumbers, x): # num*6*x^5 + num*5*x^4 + num*4*x^3 + num*3*x^2 + num*2*x + num*x + 1
    result = 0.0
    power = len(PolynomialNumbers) - 1
    for number in PolynomialNumbers[:len(PolynomialNumbers) - 2]:
        result += number * power * x**(power-1)
        power -= 1
    result += PolynomialNumbers[-2]
    return result


def newton(x, cleanPolynomialNumbers):
    return x - function(cleanPolynomialNumbers, x) / functionDerivative(cleanPolynomialNumbers, x)


def findFunctionZeroes(epsilon, n, step, window, cleanPolynomialNumbers):
    # Points that converge to zero:
    xPoints = []
    yPoints = []

    convergencePoints = []

    y = window
    while y >= -window:  # from top to bottom
        x = -window
        while x <= window:  # from left to right
            x1 = complex(x, y)
            for a in range(n-1):  # loop for n iterations
                x0 = x1
                x1 = newton(x0, cleanPolynomialNumbers)
            if abs((x0.real + x0.imag) - (x1.real + x1.imag)) < epsilon:
                xPoints.append(x) # (x, y) is the point that converges to the function zero (the x0)
                yPoints.append(y)
                convPoint = complex(round(x0.real, 3), round(x0.imag, 3))
                convergencePoints.append(convPoint)
            x += step
        y -= step

    return xPoints, yPoints, convergencePoints


def getColorArrayForScatterPlot(xPoints, yPoints, convergencePoints):
    points = list(zip(xPoints, yPoints, convergencePoints))  # points = [(x, y, (r,i))] (make an array of tuples)

    # set() stores only unique elements
    uniqueConvergencePoints = set(convergencePoints)
    # convert back to list, so that we can index items:
    uniqueConvergencePoints = list(uniqueConvergencePoints)

    # give a color to every point
    colorArray = []
    for point in points:
        convPoint = point[2]
        for i in range(
                len(uniqueConvergencePoints)):  # go through every of our convergencePoint and check which index of it corresponds to the convergent point in our points array
            if convPoint == uniqueConvergencePoints[i]:
                colorArray.append(colors[i])
                break

    return colorArray


def plot(xPoints, yPoints, colorArray):
    npXPoints = np.array(xPoints)
    npYPoints = np.array(yPoints)
    plt.scatter(npXPoints, npYPoints, c=colorArray)
    plt.show()

def plot_polynomial_graph():
    polynomial_numbers = [int(entry_fields[i].get()) for i in range(7)]
    clean_polynomial_numbers = eraseLeadingZeros(polynomial_numbers)

    x_points, y_points, convergence_points = findFunctionZeroes(
        EPSILON, N, STEP, WINDOW, clean_polynomial_numbers)
    
    color_array = getColorArrayForScatterPlot(x_points, y_points, convergence_points)

    np_x_points = np.array(x_points)
    np_y_points = np.array(y_points)

    plt.scatter(np_x_points, np_y_points, c=color_array)
    plt.show()

# Create the main window
root = tk.Tk()
root.title("Newton's Method Visualization")

# Entry fields for polynomial parameters
label = Label(root, text=f"POLYNOM", font="bald")
label.grid(row=0, column=0)

for i in range(7):
    label = Label(root, text=f"Coefficient {i + 1}:")
    label.grid(row=i + 1, column=0)
    entry = Entry(root)
    entry.grid(row=i + 1, column=1)
    entry_fields.append(entry)

label = Label(root, text=f"CONSTANTS", font="bald")
label.grid(row=8, column=0)

# Entry fields for constant values
label_n = Label(root, text=f"N:")
label_n.grid(row=9, column=0)
entry_n = Entry(root)
entry_n.grid(row=9, column=1)
entry_n.insert(0, str(N))

label_epsilon = Label(root, text=f"EPSILON:")
label_epsilon.grid(row=10, column=0)
entry_epsilon = Entry(root)
entry_epsilon.grid(row=10, column=1)
entry_epsilon.insert(0, str(EPSILON))

label_step = Label(root, text=f"STEP:")
label_step.grid(row=11, column=0)
entry_step = Entry(root)
entry_step.grid(row=11, column=1)
entry_step.insert(0, str(STEP))

label = Label(root, text=f"")
label.grid(row=12, column=0)

# Button to plot the graph
plot_button = Button(root, text="Plot Graph", command=plot_polynomial_graph)
plot_button.grid(row=13, column=0, columnspan=2)

# Create a Matplotlib Figure and an Axes object for the colorbar
fig = Figure()
ax = fig.add_subplot(111)

# Create an initial scatter plot (empty)
scatter_plot = ax.scatter([], [], c=[], cmap="jet")
ax.set_xlim(-WINDOW, WINDOW)
ax.set_ylim(-WINDOW, WINDOW)

# Create a colorbar
colorbar = fig.colorbar(scatter_plot, ax=ax)
colorbar.set_label("Convergence")

root.mainloop()