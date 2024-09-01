# # Part I : Trading strategy

import pandas as pd
import matplotlib.pyplot as plt
import re

def parse_gap_data(file_path):
    gaps = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'Gap of (\d+)s found between (\d+) and (\d+)', line)
            if match:
                gap_info = {
                    'duration': int(match.group(1)),
                    'start_time': match.group(2),
                    'end_time': match.group(3)
                }
                gaps.append(gap_info)
    return gaps

def handle_gaps(data, gap_data):
    # Defining the logic to handle data gaps by using the parsed gap information
    for gap in gap_data:
        start_time = pd.to_datetime(gap['start_time'], format='%Y%m%d%H%M%S')
        end_time = pd.to_datetime(gap['end_time'], format='%Y%m%d%H%M%S')
        # Fill or remove data within the gap period
        data.loc[(data['Timestamp'] >= start_time) & (data['Timestamp'] <= end_time)] = None

# Loading EUR/USD tick data from CSV file
eurusd_data = pd.read_csv(r"C:\Users\rapha\OneDrive\Bureau\UK\MSc Comp. Fin\S2\High-Frequency Finance\CW\CW2\Data\DAT_ASCII_EURUSD_T_201912.csv", header=None, names=['Timestamp', 'Bid', 'Ask', 'Volume'])
eurgbp_data = pd.read_csv(r"C:\Users\rapha\OneDrive\Bureau\UK\MSc Comp. Fin\S2\High-Frequency Finance\CW\CW2\Data\DAT_ASCII_EURGBP_T_201606.csv", header=None, names=['Timestamp', 'Bid', 'Ask', 'Volume'])

# Converting timestamp column to datetime format
eurusd_data['Timestamp'] = pd.to_datetime(eurusd_data['Timestamp'], format='%Y%m%d %H%M%S%f')
eurgbp_data['Timestamp'] = pd.to_datetime(eurgbp_data['Timestamp'], format='%Y%m%d %H%M%S%f')

# Calculation of the intrinsic time (eg. milliseconds since the start of trading)
eurusd_data['Intrinsic_Time'] = (eurusd_data['Timestamp'] - eurusd_data['Timestamp'].min()).dt.total_seconds() * 1000
eurgbp_data['Intrinsic_Time'] = (eurgbp_data['Timestamp'] - eurgbp_data['Timestamp'].min()).dt.total_seconds() * 1000

# Loading of the gap data
gap_eurusd = parse_gap_data(r"C:\Users\rapha\OneDrive\Bureau\UK\MSc Comp. Fin\S2\High-Frequency Finance\CW\CW2\Data\DAT_ASCII_EURUSD_T_201912.txt")
gap_eurgbp = parse_gap_data(r"C:\Users\rapha\OneDrive\Bureau\UK\MSc Comp. Fin\S2\High-Frequency Finance\CW\CW2\Data\DAT_ASCII_EURGBP_T_201606.txt")

# Handling data gaps
handle_gaps(eurusd_data, gap_eurusd)
handle_gaps(eurgbp_data, gap_eurgbp)


# Application of the trading strategy
def apply_strategy(data, lookback_period, entry_threshold):
    signals = []
    positions = []
    for i in range(len(data)):
        if i < lookback_period:
            signals.append(0)  # No signal during the initial lookback period
            positions.append(0)  # No position during the initial lookback period
        else:
            price_change = data['Ask'].iloc[i] - data['Ask'].iloc[i - lookback_period]
            if abs(price_change) > entry_threshold:
                if price_change > 0:
                    signals.append(1)  # Buy signal
                else:
                    signals.append(-1)  # Sell signal
            else:
                signals.append(0)  # No signal

            if len(positions) > 0:
                if signals[-1] == 1 and positions[-1] <= 0:
                    positions.append(1)  # Buy
                elif signals[-1] == -1 and positions[-1] >= 0:
                    positions.append(-1)  # Sell
                else:
                    positions.append(0)  # Hold
    return signals, positions

# Define strategy parameters
lookback_period = 1000  
entry_threshold = 0.0001  

eurusd_signals, eurusd_positions = apply_strategy(eurusd_data, lookback_period, entry_threshold)
eurgbp_signals, eurgbp_positions = apply_strategy(eurgbp_data, lookback_period, entry_threshold)

