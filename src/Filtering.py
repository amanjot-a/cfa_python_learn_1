
from tabulate import tabulate
import pandas as pd

investor_df= pd.read_csv(r"D:\CFA\Syllabus\_Python\charts\investors_data.csv")  


print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
print("Data has been loaded successfully")
print("  ")
print("  ")



loyal_investors_df = investor_df[investor_df['Years with Investment Firm'] >= 10]
print(tabulate(loyal_investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The code above filters the investor_df DataFrame to include only those rows where the 'Years with Investment Firm' column has a value of 10 or more. This is done using boolean indexing, where we create a boolean mask that checks the condition and then apply it to the DataFrame to get the desired subset of data.   
print("The number of investors with 10 or more years with the firm is", len(loyal_investors_df))
print("  ")
print("  ")



loyal_investors_df.reset_index(drop=True, inplace=True)
print(tabulate(loyal_investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The reset_index() method is used to reset the index of the loyal_investors_df 
# DataFrame after filtering. The drop=True argument is used to drop the old index instead of adding it as a new column, and inplace=True modifies the original DataFrame directly. This will give us a clean, sequential index for the filtered DataFrame.
print("The index has been reset for the loyal_investors_df DataFrame.")
print("  ")
print("")


investor_df.sort_values(by='Portfolio Size')
print(tabulate(investor_df.sort_values(by='Portfolio Size'), headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The sort_values() method is used to sort the investor_df DataFrame based on the values
# in the 'Portfolio Size' column. By default, it sorts in ascending order. This will rearrange the rows of the DataFrame so that the investors with smaller portfolio sizes appear first, and those with larger portfolio sizes appear later.
print("This data has been sorted by Portfolio Size in ascending order.")
print("  ")
print("  ")



investor_df
print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The code above simply prints the original investor_df DataFrame in a formatted table. This allows
# us to see the data in its original order, without any filtering or sorting applied. It serves as a reference point to compare with the filtered and sorted versions of the DataFrame.
print("This is the original investor_df DataFrame, displayed in its original order.")
print("  ")
print("  ")



investor_df.sort_values(by = 'Portfolio Size', inplace = True) 
print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The sort_values() method is used again to sort the investor_df DataFrame by the 'Portfolio Size' column, but this time with the inplace=True argument. This means that the original DataFrame will be modified directly, and the sorted order will be reflected in the investor_df variable itself. After sorting, we print the DataFrame to see the changes.
print("The investor_df DataFrame has been sorted by Portfolio Size in ascending order, and the changes have been applied to the original DataFrame due to the inplace=True argument.")
print("  ")
print("  ")



investor_df.sort_values(by = 'Age', ascending=False, inplace = True)
print(tabulate(investor_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The sort_values() method is used once again to sort the investor_df DataFrame, this time by the 'Age' column. With inplace=True, the original DataFrame is modified directly, and the rows will be rearranged in descending order based on the investors' ages. After sorting, we print the DataFrame to see the new order.
print("The investor_df DataFrame has been sorted by Age in descending order, and the changes have been applied to the original DataFrame due to the inplace=True argument.")
print("  ")     
print("  ")


High_net_worth_investors_df = investor_df[investor_df['Portfolio Size'] >= 500000]
print(tabulate(High_net_worth_investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The code above filters the investor_df DataFrame to include only those rows where the 'Portfolio Size' column has a value of 500,000 or more. This is done using boolean indexing, where we create a boolean mask that checks the condition and then apply it to the DataFrame to get the desired subset of data. This will give us a new DataFrame called High_net_worth_investors_df that contains only the high net worth investors.
print("The number of high net worth investors with a portfolio size of 500,000 or more is", len(High_net_worth_investors_df))
print("  ")
print("  ")

High_net_worth_investors_df.sum()
print("The total portfolio size of the high net worth investors is", High_net_worth_investors_df['Portfolio Size'].sum())
# The sum() method is used to calculate the total portfolio size of the high net worth investors
# by summing the values in the 'Portfolio Size' column of the High_net_worth_investors_df DataFrame. This will give us an aggregate value that represents the combined portfolio size of all the high net worth investors in our filtered DataFrame.
print("  ") 