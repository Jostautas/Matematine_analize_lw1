import matplotlib.pyplot as plt
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

    y = window
    while y > -window:
        x = -window
        while x < window:
            x1 = complex(x, y)
            for a in range(n-1):
                x0 = x1
                x1 = newton(x0, cleanPolynomialNumbers)
            if abs((x0.real + x0.imag) - (x1.real + x1.imag)) < epsilon:
                xPoints.append(x)
                yPoints.append(y)
            x += step
        y -= step

    return xPoints, yPoints



polynomialNumbers = enterPolynomial()
print("input:", polynomialNumbers)
cleanPolynomialNumbers = eraseLeadingZeros(polynomialNumbers)
#printFormula(cleanPolynomialNumbers)

EPSILON = 10**(-8)
N = 8
STEP = 0.04
WINDOW = 2 # window size to every direction from starting coordinate (0, 0)

# print(function(cleanPolynomialNumbers, complex(1, 1)))
# print(functionDerivative(cleanPolynomialNumbers, complex(1, 1)))



xPoints, yPoints = findFunctionZeroes(EPSILON, N, STEP, WINDOW, cleanPolynomialNumbers)

# print(xPoints)
# print(yPoints)

npXPoints = np.array(xPoints)
npYPoints = np.array(yPoints)


plt.plot(npXPoints, npYPoints, 'rs') # red square
plt.show()


# z = complex(1, -1)
#
# print(z)
# print(z.real)
# print(z.imag)
# print(z**5)
