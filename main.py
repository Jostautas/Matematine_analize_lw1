import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


def enterPolynomial():
    polynomialNumbers = []
    for x in range(7):
        stringInput = input(f"Enter polynomial number of index {x + 1} (counting from left):")
        try:
            intInput = int(stringInput)
            polynomialNumbers.append(intInput)
        except ValueError:
            print("Invalid integer!")
    return polynomialNumbers


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


EPSILON = 10**(-8)
N = 8
STEP = 0.04
WINDOW = 2 # window size to every direction from starting coordinate (0, 0)
colors = ["red", "blue", "yellow", "green", "magenta", "brown"]


polynomialNumbers = enterPolynomial()
cleanPolynomialNumbers = eraseLeadingZeros(polynomialNumbers)
# printFormula(cleanPolynomialNumbers)

xPoints, yPoints, convergencePoints = findFunctionZeroes(EPSILON, N, STEP, WINDOW, cleanPolynomialNumbers)

colorArray = getColorArrayForScatterPlot(xPoints, yPoints, convergencePoints)

plot(xPoints, yPoints, colorArray)
