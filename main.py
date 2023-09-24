import matplotlib.pyplot as plt
import numpy as np

# xpoints = np.array([0, 6])
# ypoints = np.array([0, 250])
#
# plt.plot(xpoints, ypoints)
# plt.show()


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


polynomialNumbers = enterPolynomial()

print("input:", polynomialNumbers)

cleanPolynomialNumbers = eraseLeadingZeros(polynomialNumbers)
formulaString = ""
power = len(cleanPolynomialNumbers) - 1
for number in cleanPolynomialNumbers[:len(cleanPolynomialNumbers)-1]:
    formulaString += f"{number}x^{power} + "
    power -= 1
formulaString += f"{cleanPolynomialNumbers[-1]}"
print("The formula:")
print(formulaString)
