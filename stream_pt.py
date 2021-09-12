from pair_trading import *
import streamlit as st
import matplotlib.pyplot as plt



start_date = '2020-08-01'
end_date = datetime.datetime.today()
TICKER = ['URTH','VEA', 'VPL', 'EPP', 'VGK', 'IEMG', 'GMF', 'SPY', 'QQQ', 'ILF', 'EWZ', 'EWW', 'EWC', 'EWH'
          ,'GXC', 'INDY', 'EWA', 'EWG','EWU', 'EWQ', 'EWM', 'VNM', 'EWL']
window = 120
stdev = 1.2


df = get_data(TICKER, start_date, end_date)
best_pairs =  get_cointegrated_pairs(df)[1]
# 'INDY','EWA' : '2014-10-01'
# 'VPL' ,'IEMG' : '2015-10-01'
pairs = ['EWA','EWC']
pairs_df = df.loc[:, pairs]
bb = get_bollinger_band(pairs_df, window, stdev)
pt_signal = get_pt_signal(df, pairs_df, bb)
pt_return =get_pt_return(df,pt_signal)
target_signal = pt_signal[[pairs_df.keys()[0],pairs_df.keys()[1]]]


# chart
fig = plt.figure(figsize = (25,20))
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
bb[bb['ratio']>bb['upper']]['ratio'].plot(color='r', linestyle='None', marker='^', label = pairs_df.keys()[1])
bb[bb['ratio']<bb['lower']]['ratio'].plot(color='g', linestyle='None', marker='v', label = pairs_df.keys()[0])

ax4 = fig.add_subplot(413, ylabel='Cumulative Compounded Returns for Pair_traing strategy')
ax4.plot((1 + pt_return).cumprod() - 1, label = 'Pair_Trading')

ax5 = fig.add_subplot(414, ylabel='Cross-Sectional Weights')
ax5.stackplot(target_signal.index, np.transpose(target_signal),labels = target_signal.columns)
plt.legend()
plt.show()
