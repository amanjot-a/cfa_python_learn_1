Company_name="Apple"
revenue=394.32
number_of_employees=154000
pays_dividends=True
type(number_of_employees)
number_of_employees=number_of_employees+2
# print(number_of_employees)



balance=5000
Share_price=142.5
# print("number of shares that can be purchased with the balance:", balance//Share_price)
# print("remaining balance after purchasing shares:", balance%Share_price)


revenue=394.32
year=2023
# print("Apple Inc. has a revenue of ${} billion in {}".format(394.32, year))

# print("Apple has an Annual of ${} billion in {}".format(revenue ,  year))

Company_symbol="P&G"
reporting_standard="US GAAP"
amount_sold=500000
#print("Procter and Gample ({}), which reports using {}, sold a piece of lan to Apple for ${}".format(Company_symbol, reporting_standard, amount_sold))

#name=input("Enter your name: ")
#print("Hi {}, how can I help you today?".format(name))


#Net Earnings = Sales Revenue * Net Profit Margin
#Dividend Per Share = (Net Earnings * Dividend Payout Ratio) / Number of Outstanding Shares


sales_revenue=float(input("Enter the sales revenue: "))
net_profit_margin=float(input("Enter the net profit margin (in %): "))
divident_payout_ratio=float(input("Enter the dividend payout ratio (in %): "))
num_outstanding_shares=float(input("Enter the number of outstanding shares: "))

net_earnings=sales_revenue * (net_profit_margin/100)
paid_dividends=net_earnings * (divident_payout_ratio/100)
dividend_per_share=(net_earnings * (divident_payout_ratio/100)) / num_outstanding_shares

print("The Company's Net Earnings is: ${:.2f}".format(net_earnings))
print("The total dividends paid by the company is: ${:.2f}".format(paid_dividends))
print("The Dividend Per Share is: ${:.2f}".format(dividend_per_share))
