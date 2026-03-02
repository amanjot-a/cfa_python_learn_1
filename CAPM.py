Stock= input("Please enter the Name of the stock: ")
Beta= float(input("Please enter the beta of the stock: "))
Risk_free_rate= float(input("Please enter the risk free rate (in %): "))
Market_return= float(input("Please enter the expected market return (in %): "))

CAPM= Risk_free_rate + Beta * (Market_return - Risk_free_rate)

print("The expected return of the stock using CAPM is: {:.2f}%".format(CAPM))
