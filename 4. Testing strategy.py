# As we explained previously, we are using the two tick data files (EUR/USD and EUR/GBP) from KEATS to backtest our trading strategy. We already loaded the given data, defined the functions and the overall code for our strategy, and we just have to run the strategy on our two datasets. 


# EUR/USD signals and position visualization
plt.figure(figsize=(12, 6))
plt.plot(eurusd_data['Intrinsic_Time'], eurusd_data['Ask'], label='EUR/USD ask price', color='green', linewidth=1)
plt.scatter(eurusd_data['Intrinsic_Time'], eurusd_data['Ask'], marker='o', c=eurusd_signals, cmap='coolwarm')
plt.xlabel('Intrinsic time (milliseconds)')
plt.ylabel('Ask Price')
plt.title('Trading strategy signals for EUR/USD')
plt.legend()
plt.colorbar(label='Signal (Buy: 1, Sell: -1, Hold: 0)')
plt.show()



# EUR/GBP signals and position visualization
plt.figure(figsize=(12, 6))
plt.plot(eurgbp_data['Intrinsic_Time'], eurgbp_data['Ask'], label='EUR/GBP ask price', color='green', linewidth=1)
plt.scatter(eurgbp_data['Intrinsic_Time'], eurgbp_data['Ask'], marker='o', c=eurgbp_signals, cmap='coolwarm')
plt.xlabel('Intrinsic time (milliseconds)')
plt.ylabel('Ask')
plt.title('Trading strategy signals for EUR/GBP')
plt.legend()
plt.colorbar(label='Signal (Buy: 1, Sell: -1, Hold: 0)')
plt.show()
