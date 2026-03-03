import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Load the data
# Adjust the file paths if the CSVs are extracted to a different directory
amzn_df = pd.read_csv('Amazon.csv')
jpm_df = pd.read_csv('JPM.csv')

# 2. Clean and merge the data
amzn_df['Date'] = pd.to_datetime(amzn_df['Date'])
jpm_df['Date'] = pd.to_datetime(jpm_df['Date'])

amzn_df.set_index('Date', inplace=True)
jpm_df.set_index('Date', inplace=True)

# Combine 'Adj Close' prices into a single DataFrame
# An inner join aligns the dates automatically
portfolio_df = pd.concat([amzn_df['Adj Close'], jpm_df['Adj Close']], axis=1, join='inner')
portfolio_df.columns = ['AMZN', 'JPM']

# 3. Calculate simple daily returns
returns = portfolio_df.pct_change().dropna()

# 4. Monte Carlo Simulation Setup
num_portfolios = 10000
trading_days = 252
risk_free_rate = 0.02 # Assuming a 2% risk-free rate for the Sharpe calculation

# Arrays to store the simulation results
all_weights = np.zeros((num_portfolios, len(portfolio_df.columns)))
ret_arr = np.zeros(num_portfolios)
vol_arr = np.zeros(num_portfolios)
sharpe_arr = np.zeros(num_portfolios)

mean_returns = returns.mean()
cov_matrix = returns.cov()

# Run the simulation
for i in range(num_portfolios):
    # Generate random weights that sum to 1
    weights = np.random.random(len(portfolio_df.columns))
    weights /= np.sum(weights)
    all_weights[i, :] = weights
    
    # Expected Annualized Return
    portfolio_return = np.sum(mean_returns * weights) * trading_days
    ret_arr[i] = portfolio_return
    
    # Expected Annualized Volatility (Risk)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(trading_days)
    vol_arr[i] = portfolio_volatility
    
    # Sharpe Ratio
    sharpe_arr[i] = (portfolio_return - risk_free_rate) / portfolio_volatility

# 5. Identify the Optimal Portfolio (Maximum Sharpe Ratio)
max_sharpe_idx = sharpe_arr.argmax()
optimal_weights = all_weights[max_sharpe_idx, :]
max_sharpe_return = ret_arr[max_sharpe_idx]
max_sharpe_volatility = vol_arr[max_sharpe_idx]

print("=== OPTIMAL PORTFOLIO ALLOCATION ===")
print(f"Amazon (AMZN) Weight: {optimal_weights[0]*100:.2f}%")
print(f"JPMorgan (JPM) Weight: {optimal_weights[1]*100:.2f}%")
print(f"Expected Annualized Return: {max_sharpe_return*100:.2f}%")
print(f"Expected Annualized Volatility (Risk): {max_sharpe_volatility*100:.2f}%")
print(f"Maximum Sharpe Ratio: {sharpe_arr[max_sharpe_idx]:.2f}")

# 6. Plot the Efficient Frontier
plt.figure(figsize=(10, 6))
plt.scatter(vol_arr, ret_arr, c=sharpe_arr, cmap='viridis', marker='o', s=10, alpha=0.3)
plt.colorbar(label='Sharpe Ratio')

# Mark the optimal portfolio with a red star
plt.scatter(max_sharpe_volatility, max_sharpe_return, c='red', marker='*', s=300, edgecolor='black', label='Max Sharpe Portfolio')

plt.title('Monte Carlo Simulation: Portfolio Optimization')
plt.xlabel('Expected Annualized Volatility (Risk)')
plt.ylabel('Expected Annualized Return')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()