import sys

import pandas as pd
import numpy as np
from tabulate import tabulate

investor_df = pd.read_csv(r"D:\CFA\Syllabus\_Python\charts\investors_data.csv")

print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The code above loads the investors_data.csv file into a pandas DataFrame called investors_df and
# then prints the DataFrame in a formatted table using the tabulate library. The headers='keys' argument specifies that the column names should be used as headers, and the tablefmt='fancy_grid' argument specifies the format of the table. The stralign and numalign arguments are used to align string and numeric data in the table, respectively. This allows us to visualize the data in a more organized and readable way.
print("Data has been loaded successfully")
print("  ")



def portfolio_update(portfolio_size):return portfolio_size * 1.05
# The code above defines a function called portfolio_update that takes a single argument, portfolio_size.

investor_df['Updated Portfolio Size'] = investor_df['Portfolio Size'].apply(portfolio_update)
print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
print("The 'Updated Portfolio Size' column has been added to the investor_df DataFrame, with values calculated by applying the portfolio_update function to the 'Portfolio Size' column.")
print("  ")



def years_update(years): return years + 1
# The code above defines a function called years_update that takes a single argument, years. This function simply adds 1 to the input value, which can be used to update the 'Years with Investment Firm' column in the DataFrame.
investor_df['Updated Years'] = investor_df['Years with Investment Firm'].apply(years_update)
print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
print("The 'Updated Years' column has been added to the investor_df DataFrame, with values calculated by applying the years_update function to the 'Years with Investment Firm' column.")
print("  ")

