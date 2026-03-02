# This program calculates the number of years required for an investment to grow from a present value (PV) to a future value (FV) given an annual interest rate. It also prints the future value of the investment at the end of each year until it reaches or exceeds the target future value.
# The program uses a while loop to calculate the future value of the investment at the end of each year and prints it. It also checks for invalid input where the future value must be greater than the present value.
# The program uses the logarithm function from the math module to calculate the number of years required for the investment to grow to the future value.
# The user is prompted to enter the present value, annual interest rate, and future value of the investment. The program then calculates and prints the number of years required for the investment to grow to the future value, as well as the future value at the end of each year.
# The program also includes error handling to ensure that the future value entered by the user is greater than the present value, and it continues to prompt the user until valid input is provided.
# The program demonstrates the use of while loops, user input, and mathematical calculations in Python. It also includes formatted output to display the results in a clear and concise manner.
# The program can be used to help investors understand how long it will take for their investments to grow to a desired future value based on the present value and annual interest rate. It can also be used as a learning tool for understanding the concept of compound interest and the time value of money in finance.


import math

from matplotlib.pyplot import plot

PV = float(input("Please enter the present value of the investment: "))
Interest = float(input("Please enter the annual interest rate (in %): "))
FV = float(input("Please enter the future value of the investment: "))

N = math.log(FV / PV) / math.log(1 + Interest / 100)

while N < 0:
    print("Invalid input. Future value must be greater than present value.")
    FV = int(input("Please enter the future value of the investment: "))
    N = math.log(FV / PV) / math.log(1 + Interest / 100)

year = 0
current_value = PV

# Print Year 0
print(f"\nPV in Year {year} (now) = ${current_value:.1f}")

# Loop until we exceed target
while current_value < FV:
    year += 1
    current_value = PV * (1 + Interest / 100) ** year
    print(f"FV of the investmeant at the end of Year {year} would be: ${current_value:.1f}")

print("The number of years required is: {:.0f}".format(N))

plot(year, current_value, marker='o')
plot(N, FV, marker='o') 