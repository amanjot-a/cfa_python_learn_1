# Handling missing data in pandas DataFrames

import pandas as pd
from tabulate import tabulate

investors_df = pd.read_csv(r"D:\CFA\Syllabus\_Python\charts\investors_data.csv")

print(tabulate(investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))

# fancy grid, yayy

print(investors_df.isnull().sum())
# The isnull() method is used to check for missing values in the DataFrame. It returns a DataFrame of the same shape with boolean values indicating whether each entry is null (True) or not (False). The sum() method is then used to count the number of missing values in each column.


# investors_df.dropna(how='any' , inplace=True)
print(tabulate(investors_df.dropna(how='any'), headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# # The dropna() method is used to remove rows with missing values. The how='any' argument specifies that any row with at least one missing value should be dropped. The inplace=True argument modifies the original DataFrame.



# print(investors_df.isnull().sum())

# The dropna() method is used to remove rows with missing values. The how='any
# argument specifies that any row with at least one missing value should be dropped. The inplace=True argument modifies the original DataFrame.

print(tabulate(investors_df.describe() , headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))

print("  ")
print("  ")

investors_df['Portfolio Size'].mean()
print("Mean of Portfolio Size column is", investors_df['Portfolio Size'].mean().__format__('.0f'))
# The mean() method is used to calculate the average of the values in the 'Portfolio Size' column. The __format__('.0f') is used to format the output as a floating-point number with no decimal places.
print("  ")
print("  ")
print(investors_df['Portfolio Size'].fillna(investors_df['Portfolio Size'].mean(), inplace=True))
print(tabulate(investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# The fillna() method is used to fill missing values in a column. In this case, we are filling the missing values in the 'Portfolio Size' column with the mean of that column. This is a common technique for handling missing data, as it allows us to retain all rows while providing a reasonable estimate for the missing values.

print(investors_df.info())

print("  ")
print("  ")
print(investors_df.isnull().sum())
# After filling the missing values, we can check again for any remaining null values using the isnull().sum() method. This will confirm that all missing values have been handled appropriately.
investors_df['Years with Investment Firm'].median()
print("Median of Years with Investment Firm column is", investors_df['Years with Investment Firm'].median())
# The median() method is used to calculate the median of the values in the 'Years with Investment Firm' column. The median is the middle value when the data is sorted, and it is less affected by outliers compared to the mean. This can be a better choice for filling missing values in cases where the data may have extreme values.

print(investors_df['Years with Investment Firm'].fillna(investors_df['Years with Investment Firm'].median(), inplace=True))
print(tabulate(investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))
# Similar to the previous fillna() method, we are filling the missing values in the 'Years with Investment Firm' column with the median of that column. This allows us to handle the missing data while retaining all rows in the DataFrame.    


print(investors_df.isnull().sum())
# The sum() method is used to calculate the sum of the values in each column. This can be useful for getting a quick overview of the total values in the DataFrame, especially after handling missing data.