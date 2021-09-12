from pair_trading import *
import streamlit as st
import matplotlib.pyplot as plt


st.title('Pair-Trading Backtesting')

st.write('Backtest pair-trading strategies using Price, SignalMetric, Return, Weight chart')

start_date = st.date_input('Select start_date')
end_date = end_date = datetime.datetime.today()

TICKER_1 = {'MSCI WORLD' : 'URTH',
          'Developed Market' : 'VEA',
          'Asia' : 'VPL',
          'Asia w/o JPN' : 'EPP',
          'Europe' : 'VGK',
          'Emerging Market' : 'IEMG',
          'Asia Emerging' : 'GMF',
          'S&P' : 'SPY',
          'NASDAQ' : 'QQQ',
          'Latin America' : 'ILF',
          'Brazil' : 'EWZ',
          'Mexico' : 'EWW',
          'Canada' : 'EWC',
          'Hongkong' : 'EWH',
          'China' : 'GXC',
          'Japan' : 'EWJ',
          'India' : 'INDY',
          'Vietnam' : 'VNM',
          'Austrailia' : 'EWA',
          'Germany' : 'EWG',
          'England' : 'EWU',
          'France' : 'EWQ'}
selected_stock_key_1 = st.selectbox('Select "TICKER1" you want to backtest', list(TICKER_1.keys()))
selected_stock_value_1 = TICKER_1[selected_stock_key_1]


TICKER_2 = {'MSCI WORLD' : 'URTH',
          'Developed Market' : 'VEA',
          'Asia' : 'VPL',
          'Asia w/o JPN' : 'EPP',
          'Europe' : 'VGK',
          'Emerging Market' : 'IEMG',
          'Asia Emerging' : 'GMF',
          'S&P' : 'SPY',
          'NASDAQ' : 'QQQ',
          'Latin America' : 'ILF',
          'Brazil' : 'EWZ',
          'Mexico' : 'EWW',
          'Canada' : 'EWC',
          'Hongkong' : 'EWH',
          'China' : 'GXC',
          'Japan' : 'EWJ',
          'India' : 'INDY',
          'Vietnam' : 'VNM',
          'Austrailia' : 'EWA',
          'Germany' : 'EWG',
          'England' : 'EWU',
          'France' : 'EWQ'}
selected_stock_key_2 = st.selectbox('Select "TICKER2" you want to backtest', list(TICKER_2.keys()))
selected_stock_value_2 = TICKER_2[selected_stock_key_2]

pairs = [selected_stock_value_1, selected_stock_value_2]

window = 120
stdev = 1.2


df = get_data(pairs, start_date, end_date)
pairs_df = df.loc[:, pairs]
bb = get_bollinger_band(pairs_df, window, stdev)
pt_signal = get_pt_signal(df, pairs_df, bb)
pt_return =get_pt_return(df,pt_signal)
target_signal = pt_signal[[pairs_df.keys()[0],pairs_df.keys()[1]]]


# chart
fig = plt.figure(figsize = (45,40))
ax1 = fig.add_subplot(411, ylabel='Pair Prices in $')
ax2 = ax1.twinx()
ax1.plot(pairs_df[pairs_df.keys()[0]], color = 'dodgerblue', label = pairs_df.keys()[0])
ax2.plot(pairs_df[pairs_df.keys()[1]], color = 'orangered', label = pairs_df.keys()[1])
ax1.set_ylabel(pairs_df.keys()[0])
ax1.legend(loc = 'upper left')
ax2.legend(loc = 'lower right')
ax2.set_ylabel(pairs_df.keys()[1])

ax3 = fig.add_subplot(412, ylabel='Relative Ratio for Pair Prices')
bb['ratio'].plot(color = 'paleturquoise')
bb['upper'].plot(linestyle='--')
bb['lower'].plot(linestyle='--')
ax3.plot(bb[bb['ratio']>bb['upper']]['ratio'], color='r', linestyle='None', marker='^', label = pairs_df.keys()[1])
ax3.plot(bb[bb['ratio']<bb['lower']]['ratio'], color='g', linestyle='None', marker='v', label = pairs_df.keys()[0])
ax3.legend(loc = 'upper left')

ax4 = fig.add_subplot(413, ylabel='Cumulative Compounded Returns for Pair_traing strategy')
ax4.plot((1 + pt_return).cumprod() - 1, label = 'Pair_Trading')
ax4.legend(loc = 'upper left')

ax5 = fig.add_subplot(414, ylabel='Cross-Sectional Weights')
ax5.stackplot(target_signal.index, np.transpose(target_signal),labels = target_signal.columns)
ax5.legend(loc = 'upper left')

st.pyplot(fig)

# Pair Prices
#
# fig, ax1 = plt.subplots(figsize=(15,7))
# ax2 = ax1.twinx()
# ax1.plot(pairs_df[pairs_df.keys()[0]], color = 'dodgerblue', label = pairs_df.keys()[0])
# ax2.plot(pairs_df[pairs_df.keys()[1]], color = 'orangered', label = pairs_df.keys()[1])
# ax1.set_ylabel(pairs_df.keys()[0])
# ax1.legend(loc = 'upper left')
# ax2.legend(loc = 'lower right')
# ax2.set_ylabel(pairs_df.keys()[1])
# plt.show()

# Relative Ratio for Pair Prices
# plt.figure(figsize=(15,7))
# plt.title('equity_bollinger_band')
# bb['ratio'].plot(color = 'paleturquoise')
# bb['upper'].plot(linestyle='--')
# bb['lower'].plot(linestyle='--')
# bb[bb['ratio']>bb['upper']]['ratio'].plot(color='r', linestyle='None', marker='^', label = pairs_df.keys()[1])
# bb[bb['ratio']<bb['lower']]['ratio'].plot(color='g', linestyle='None', marker='v', label = pairs_df.keys()[0])
# plt.legend()
# plt.show()


# Cumulative Compounded Returns for Pair_traing strategy
# plt.figure(figsize=(17,7))
# plt.title('Pair Trading Strategy Return')
# plt.plot((1 + pt_return).cumprod() - 1, label = 'Pair_Trading')
# plt.legend()
# plt.show()

# Cross-Sectional Weights
# target_signal = pt_signal[[pairs_df.keys()[0],pairs_df.keys()[1]]]
# plt.figure(figsize=(17,7))
# plt.title('Cross-Sectional Weights')
# plt.stackplot(target_signal.index, np.transpose(target_signal),labels = target_signal.columns)
# plt.legend()
# plt.show()


