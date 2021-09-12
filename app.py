from pair_trading import *
import streamlit as st
import matplotlib.pyplot as plt


st.title('Pair-Trading Backtesting')

st.write('Backtest pair-trading strategies using chart')

start_date = st.date_input('Select start_date')
end_date = end_date = datetime.datetime.today()

TICKER = {'URTH','VEA', 'VPL', 'EPP', 'VGK', 'IEMG', 'GMF', 'SPY', 'QQQ', 'ILF', 'EWZ', 'EWW', 'EWC', 'EWH'
          ,'GXC', 'INDY', 'EWA', 'EWG','EWU', 'EWQ'}
selected_stock_key = st.selectbox('Select "TICKER" you want to backtest', list(TICKER.keys()))
selected_stock_value = TICKER[selected_stock_key]



# start_date = '2020-04-01'
end_date = datetime.datetime.today()
window = 120
stdev = 1.2


df = get_data(TICKER, start_date, end_date)
pairs = ['VGK','EWC']
pairs_df = df.loc[:, pairs]
bb = get_bollinger_band(pairs_df, window, stdev)
pt_signal = get_pt_signal(df, pairs_df, bb)
pt_return =get_pt_return(df,pt_signal)

# Pair Prices

fig, ax1 = plt.subplots(figsize=(15,7))
ax2 = ax1.twinx()
ax1.plot(pairs_df[pairs_df.keys()[0]], color = 'dodgerblue', label = pairs_df.keys()[0])
ax2.plot(pairs_df[pairs_df.keys()[1]], color = 'orangered', label = pairs_df.keys()[1])
ax1.set_ylabel(pairs_df.keys()[0])
ax1.legend(loc = 'upper left')
ax2.legend(loc = 'lower right')
ax2.set_ylabel(pairs_df.keys()[1])
plt.show()

# Relative Ratio for Pair Prices
plt.figure(figsize=(15,7))
plt.title('equity_bollinger_band')
bb['ratio'].plot(color = 'paleturquoise')
bb['upper'].plot(linestyle='--')
bb['lower'].plot(linestyle='--')
bb[bb['ratio']>bb['upper']]['ratio'].plot(color='r', linestyle='None', marker='^', label = pairs_df.keys()[1])
bb[bb['ratio']<bb['lower']]['ratio'].plot(color='g', linestyle='None', marker='v', label = pairs_df.keys()[0])
plt.legend()
plt.show()


# Cumulative Compounded Returns for Pair_traing strategy
plt.figure(figsize=(17,7))
plt.title('Pair Trading Strategy Return')
plt.plot((1 + pt_return).cumprod() - 1, label = 'Pair_Trading')
plt.legend()
plt.show()

# Cross-Sectional Weights
target_signal = pt_signal[[pairs_df.keys()[0],pairs_df.keys()[1]]]
plt.figure(figsize=(17,7))
plt.title('Cross-Sectional Weights')
plt.stackplot(target_signal.index, np.transpose(target_signal),labels = target_signal.columns)
plt.legend()
plt.show()