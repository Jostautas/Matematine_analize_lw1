import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Entry, Button, Label, Frame
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import ListedColormap

# Define entryFields
entryFields = []

# Constants and colors
# N = 30
EPSILON = 1e-6
# STEP = 0.03
WINDOW = 2
colors = ["red", "blue", "yellow", "green", "magenta", "lime", "purple", "aqua", "pink", "cyan", "olive"]

# Function to erase leading zeros in the polynomial numbers
def eraseLeadingZeros(PolynomlialNumbers):
    return PolynomlialNumbers[next((i for i, x in enumerate(PolynomlialNumbers) if x != 0), 7):]

def custom_complex_exponentiation(x, power):
    try:
        result = x**power
        return result
    except OverflowError:
        # Handle overflow cases gracefully
        return complex(float('inf'), 0.0)

# Function to calculate the function value at a given point
def function(PolynomlialNumbers, x):
    result = 0.0
    power = len(PolynomlialNumbers) - 1
    for number in PolynomlialNumbers[:len(PolynomlialNumbers) - 1]:
        result += number * custom_complex_exponentiation(x, power)
        power -= 1
    result += PolynomlialNumbers[-1]
    return result

# Function to calculate the derivative of the function
def functionDerivative(PolynomlialNumbers, x):
    result = 0.0
    power = len(PolynomlialNumbers) - 1
    for number in PolynomlialNumbers[:len(PolynomlialNumbers) - 2]:
        result += number * power * custom_complex_exponentiation(x, power - 1)
        power -= 1
    result += PolynomlialNumbers[-2]
    return result

# Function for the Newton-Raphson iteration
def newton(x, cleanPolynomialNumbers):
    return x - function(cleanPolynomialNumbers, x) / functionDerivative(cleanPolynomialNumbers, x)

# Function to find function zeroes and convergence points
def findFunctionZeroes(epsilon, n, step, window, cleanPolynomialNumbers):
    xPoints = []
    yPoints = []
    convergencePoints = []

    y = window
    while y >= -window:
        x = -window
        while x <= window:
            x1 = complex(x, y)
            for a in range(n - 1):
                x0 = x1
                x1 = newton(x0, cleanPolynomialNumbers)
            if abs((x0.real + x0.imag) - (x1.real + x1.imag)) < epsilon:
                xPoints.append(x)
                yPoints.append(y)
                convPoint = complex(round(x0.real, 3), round(x0.imag, 3))
                convergencePoints.append(convPoint)
            x += step
        y -= step
        
    return xPoints, yPoints, convergencePoints

# Function to assign colors for the scatter plot
def getColorArrayForScatterPlot(xPoints, yPoints, convergencePoints, roots):
    points = list(zip(xPoints, yPoints, convergencePoints))
    # uniqueConvergencePoints = set(convergencePoints)
    # uniqueConvergencePoints = list(uniqueConvergencePoints)
    uniqueConvergencePoints = roots
    colorArray = []
    for point in points:
        convPoint = point[2]
        for i in range(len(uniqueConvergencePoints)):
            if convPoint == uniqueConvergencePoints[i]:
                colorArray.append(colors[i])
                break
    return colorArray

# Create the main window
root = tk.Tk()

# Calculate the screen width and height for centering the window
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
windowWidth = 530  # Width of the window
windowHeight = 630  # Height of the window
x = (screenWidth - windowWidth) // 2
y = (screenHeight - windowHeight) // 2 - 30
root.geometry(f"{windowWidth}x{windowHeight}+{x}+{y}")

root.title("Polynomial Plotter")  # Set the window title

# Entry fields for polynomial parameters
polynomialDescription = "POLYNOM\n\nax⁶  +  bx⁵  +  cx⁴  +  dx³  +  ex²  +  fx¹  +  g"
label = Label(root, text=polynomialDescription, font=("Helvetica", 12, "bold"))
label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

coefficientsFrame = Frame(root)
coefficientsFrame.grid(row=1, column=0, columnspan=2)

coefficients = ["a", "b", "c", "d", "e", "f", "g"]

# Entry boxes for coefficient input
entryFrame = Frame(root)
entryFrame.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
for i, coef in enumerate(coefficients):
    label = Label(entryFrame, text=f"{coef}:", font=("Helvetica", 10))
    label.grid(row=0, column=i)
    entry = Entry(entryFrame, font=("Helvetica", 10), width=5)
    entry.grid(row=1, column=i, padx=5)
    entryFields.append(entry)

label = Label(root, text="CONSTANTS", font=("Helvetica", 12, "bold"))
label.grid(row=8, column=0, columnspan=2)

# Entry field for constant values (aligned to the middle)
labelN = Label(root, text="N:", font=("Helvetica", 10))
labelN.grid(row=9, column=0, padx=(0, 50), pady=5)
entryN = Entry(root, font=("Helvetica", 10), width=5)
entryN.grid(row=9, column=0, padx=(50, 0), pady=5)

labelStep = Label(root, text="STEP:", font=("Helvetica", 10))
labelStep.grid(row=9, column=1, padx=(100, 150), pady=5)
entryStep = Entry(root, font=("Helvetica", 10), width=5)
entryStep.grid(row=9, column=1, padx=(150, 100), pady=5)

# Create a Matplotlib Figure and an Axes object
fig = Figure(figsize=(8, 8))
ax = fig.add_subplot(111)

cmap = ListedColormap(colors)
scatterPlot = ax.scatter([], [], c=[], cmap=cmap)
ax.set_xlim(-WINDOW, WINDOW)
ax.set_ylim(-WINDOW, WINDOW)

canvas = FigureCanvasTkAgg(fig, master=root)
canvasWidget = canvas.get_tk_widget()
canvasWidget.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Create a Text widget to display convergence points
convergenceText = tk.Text(root, height=5, width=40, font=("Helvetica", 10))
convergenceText.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

# Function to plot the polynomial graph
def plotPolynomialGraph():
    # Get the user-set value for N and STEP
    n = int(entryN.get())
    step = float(entryStep.get())
    PolynomlialNumbers = [float(entryFields[i].get()) for i in range(7)]
    
    coefficientsArray = PolynomlialNumbers
    roots = np.roots(coefficientsArray)
    roots = set(roots)
    rounded_roots = [complex(round(root.real, 3), round(root.imag, 3)) for root in roots]
    
    cleanPolynomialNumbers = eraseLeadingZeros(PolynomlialNumbers)
    xPoints, yPoints, convergencePoints = findFunctionZeroes(EPSILON, n, step, WINDOW, cleanPolynomialNumbers)

    colorArray = getColorArrayForScatterPlot(xPoints, yPoints, convergencePoints, rounded_roots)
    
    colorNumericValues = [colors.index(color) for color in colorArray]

    scatterPlot.set_offsets(np.column_stack((xPoints, yPoints)))
    scatterPlot.set_array(np.array(colorNumericValues))
    scatterPlot.set_clim(vmin=0, vmax=len(colors) - 1)

    # Add the "x =" strings with convergence points
    convergenceText.delete('1.0', tk.END)
    convergenceText.insert(tk.END, "Convergence Points:\n")
    for root in roots:
        realPart = round(root.real, 3)
        imagPart = round(root.imag, 3)
        complexRoot = complex(realPart, imagPart)
        text = convergenceText.get("1.0", "end-1c")
        convergenceText.insert(tk.END, f"x = {complexRoot}\n")
        
    canvas.draw()

# Button to plot the graph
plotButton = Button(root, text="Plot Graph", font=("Helvetica", 10, "bold"), command=plotPolynomialGraph)
plotButton.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

# Configure row and column weights to make components expand with window size
root.grid_rowconfigure(12, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
