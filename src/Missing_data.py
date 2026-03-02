# Handling missing data in pandas DataFrames

import pandas as pd
from tabulate import tabulate

investors_df = pd.read_csv(r"D:\CFA\Syllabus\_Python\charts\investors_data.csv")

print(tabulate(investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center'))

print(tabulate(investors_df, headers='keys', tablefmt='fancy_grid',stralign='center', numalign='center', showindex=False))
# fancy grid, yayy




#print(investors_df.isnull)
