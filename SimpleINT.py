Days= input("Enter number of days: ")
Interest_rate= float(input("Enter the annual interest rate (in %): "))
Principal_amount= float(input("Enter the principal amount: "))
Simple_Interest= (Principal_amount * Interest_rate * int(Days)) / 36500

Compound_interest=(Principal_amount * (1 + (Interest_rate / 100))**(int(Days)/365)) - Principal_amount

print("The Simple Interest accrued over {} days is: ${:.2f}".format(Days, Simple_Interest)) 

print("The Compound Interest accrued over {} days is: ${:.2f}".format(Days, Compound_interest))
