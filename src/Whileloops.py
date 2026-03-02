## This program demonstrates the use of while loops in Python.
            # The first loop prints the numbers from 0 to 9, incrementing by 5 each time.
            # The second loop calculates the future value of an investment over 3 years with a given present value and interest rate.
            # The third loop prompts the user to enter their age and continues to ask until a valid (non-negative) age is entered.
i = 0
while i < 10:
    print(i)
    i = i + 5

PV = 1000
N = 1
Interest = 0.12

while N <=3:
    FV = PV * (1 + Interest) ** N
    print("The future value of the investment after {} year(s) is: {:.2f}".format(N, FV))
    N = N + 1

Age = 18

while Age < 0:
    print("Invalid input. Age cannot be negative.")
    Age = int(input("Please enter your age: "))



X = 1
while True:
    X = X * 2
    print('Value {}.'.format(X))
    if X > 1000:
        break