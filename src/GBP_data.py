

import matplotlib.pyplot as plt
import pandas as pd

GDP_df = pd.DataFrame({
    'Country': ['USA', 'China', 'Japan', 'Germany', 'India'],  
    'Country Code': ['US', 'CN', 'JP', 'DE', 'IN'],
    'GDP per Capita': [65000, 10000, 40000, 45000, 2000],
    'Global Rank': [5, 64, 27, 19, 142]})

print(GDP_df)

