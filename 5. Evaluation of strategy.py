import numpy as np

# Function to calculate PnL
def calculate_pnl(data, positions):
    pnl = pd.Series(0.0, index=data.index)
    for i in range(1, len(data)):
        pnl.iloc[i] = pnl.iloc[i - 1] + positions[i - 1] * (data['Ask'].iloc[i] - data['Ask'].iloc[i - 1])
    return pnl

eurusd_pnl = calculate_pnl(eurusd_data, eurusd_positions)
eurgbp_pnl = calculate_pnl(eurgbp_data, eurgbp_positions)


# - **Sharpe ratio** : measures the risk-adjusted return of the strategy by indicating the *excess return generated per unit of risk*
# 
# It it such as : 
# <center>$$ Sharpe\ Ratio = \frac{{R_p - R_f}}{{\sigma_p}} $$<center>
# <br>    
# With :<br> 
# $R_p$ the expected portfolio return<br>
# $R_f$ the risk free rate<br>
# $\sigma_p$ the standard deviation of the portfolio<br>



# Function to calculate Sharpe Ratio
def calculate_sharpe_ratio(pnl):
    daily_returns = pnl.pct_change().dropna()
    sharpe_ratio = np.sqrt(252) * (daily_returns.mean() / daily_returns.std())
    return sharpe_ratio

sharpe_ratio_eurusd = calculate_sharpe_ratio(eurusd_pnl)
sharpe_ratio_eurgbp = calculate_sharpe_ratio(eurgbp_pnl)


# - **Maximum drawdown** : measures the largest peak-to-trough decline in the equity curve of the strategy, it is the *maximum loss incurred by the strategy during the backtested period*
#     
# It it such as :
# <center>$$ Maximum\ Drawdown = \max\left(\frac{{P_i - P_j}}{{P_i}}\right) $$<center
# <br> 
# With :<br> 
# $P_i$ the trough (lowest value) of the equity curve following the peak<br>
# $P_j$ the peak (highest value) of the equity curve up to a certain point<br>                                                                                  
#                                                                            


# Function to calculate Maximum Drawdown
def calculate_max_drawdown(pnl):
    peak = pnl.iloc[0]
    max_drawdown = 0
    for i in range(1, len(pnl)):
        if pnl.iloc[i] > peak:
            peak = pnl.iloc[i]
        else:
            drawdown = (peak - pnl.iloc[i]) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    return max_drawdown

max_drawdown_eurusd = calculate_max_drawdown(eurusd_pnl)
max_drawdown_eurgbp = calculate_max_drawdown(eurgbp_pnl)



print("Sharpe ratio for EUR/USD:", sharpe_ratio_eurusd)
print("Sharpe ratio for EUR/GBP:", sharpe_ratio_eurgbp)
print("Maximum drawdown for EUR/USD:", max_drawdown_eurusd)
print("Maximum drawdown for EUR/GBP:", max_drawdown_eurgbp)

# Plot PnL for EUR/USD and EUR/GBP
plt.figure(figsize=(12, 6))
plt.plot(eurusd_data['Timestamp'], eurusd_pnl, color='blue', label='EUR/USD PnL')
plt.plot(eurgbp_data['Timestamp'], eurgbp_pnl, color='red', label='EUR/GBP PnL')
plt.xlabel('Timestamp')
plt.ylabel('PnL')
plt.title('Profit and Loss (PnL) for EUR/USD and EUR/GBP')
plt.legend()
plt.grid(True)
plt.show()


# Plot maximum drawdown for EUR/USD and EUR/GBP
plt.figure(figsize=(10, 5))
plt.bar(['EUR/USD', 'EUR/GBP'], [max_drawdown_eurusd, max_drawdown_eurgbp], color=['blue', 'red'])
plt.title('Maximum drawdown')
plt.xlabel('Currency pair')
plt.ylabel('Maximum drawdown')
plt.ylim([0, max(max_drawdown_eurusd, max_drawdown_eurgbp) + 0.1])
plt.grid(True)
plt.show()
