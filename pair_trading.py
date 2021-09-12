import numpy as np
import pandas as pd
import datetime
import pandas_datareader as pdr
from statsmodels.tsa.stattools import coint

def get_data(TICKER, start_date, end_date) :
    '''
        Parameters
                ----------
                TICKER : list
                    Target TICKER list
                start_date : datetime
                    start_date
                end_date : datetime
                    end_date
        Returns
                -------
                df : dataframe
                    Historical daily Adj Close
    '''
    df = pd.DataFrame(pdr.get_data_yahoo(TICKER, start = start_date, end = end_date)['Adj Close'])
    df.columns = TICKER
    return df

def get_cointegrated_pairs(df):
    """
         Parameters
         ----------
         prices : dataframe
             Historical daily prices
         Returns
         -------
         pairs_df : dataframe
             pairs which are identified as stationary
    """
    pvalue_matrix = np.ones((df.shape[1], df.shape[1]))
    keys = df.keys()
    pairs = pd.DataFrame()
    pairs_1 =[]
    pairs_2 =[]
    pairs_pvalue = []
    for i in range(df.shape[1]):
        for j in range(i+1, df.shape[1]):
            result = coint(df[keys[i]], df[keys[j]])
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            pairs_1.append(keys[i])
            pairs_2.append(keys[j])
            pairs_pvalue.append(pvalue)
    pairs['asset1'] = pairs_1
    pairs['asset2'] = pairs_2
    pairs['pvalue'] = pairs_pvalue
    pairs_df = pairs.loc[pairs['pvalue'].idxmin()]
    pairs_df = df.loc[:,[pairs_df['asset1'],pairs_df['asset2']]]
    return pvalue_matrix, pairs_df


def get_bollinger_band(df, window, stdev):
    """
        Parameters
        ----------
        df : dataframe
            pairs which are identified as stationary
        window : int
            look-back period
        stdev : int
            standard deviations
        Returns
        -------
        bb : dataframe
            bollingerband data for pairs relative ratio
         """
    df['ratio'] = df.iloc[:, 0] / df.iloc[:, 1]
    bb = df.copy()
    bb['center'] = df['ratio'].rolling(window).mean()
    bb['upper'] = bb['center'] + stdev * df['ratio'].rolling(window).std()
    bb['lower'] = bb['center'] - stdev * df['ratio'].rolling(window).std()
    return bb

def get_pt_signal(prices, pairs_df, bb):
    """
        Parameters
        ----------
        prices : dataframe
            Historical daily prices
        pairs_df : dataframe
            pairs which are identified as stationary
        bb : dataframe
            Historical bollinger-band data
        Returns
        -------
        signal : dataframe
            pair trading signals
    """
    bb['1'] = 0
    bb['2'] = 0
    for i in bb.index:
        if bb['ratio'][i] > bb['upper'][i]:
            bb.loc[i, '1'] = 0
            bb.loc[i, '2'] = 1
        elif bb['upper'][i] > bb['ratio'][i] and bb['ratio'][i] > bb['lower'][i]:
            if bb.shift(1)['1'][i] == 1:
                bb.loc[i, '1'] = 1
                bb.loc[i, '2'] = 0
            else:
                bb.loc[i, '1'] = 0
                bb.loc[i, '2'] = 1
        elif bb['lower'][i] > bb['ratio'][i]:
            bb.loc[i, '1'] = 1
            bb.loc[i, '2'] = 0
    book = pd.DataFrame(bb[['ratio', '1', '2']])
    book = book.rename(columns={'1': pairs_df.keys()[0], '2': pairs_df.keys()[1]})
    signal = pd.DataFrame(index=prices.index, columns=prices.columns).fillna(value=0)
    signal[pairs_df.keys()[0]] = book[pairs_df.keys()[0]].fillna(0)
    signal[pairs_df.keys()[1]] = book[pairs_df.keys()[1]].fillna(0)
    signal = (signal.shift(1)).fillna(0)
    return signal

def get_pt_return(df, pt_signal):
    """
        Parameters
        ------------
        df: dataframe
           Historical daily Price
        signal: dataframe
           Historical daily Absolute Momentum Signal

        Returns
        ------------
        am_result : dataframe
            Absolute Momentum Portfolio return
    """
    df_rtn = df.pct_change().fillna(0)
    pt_return = pd.DataFrame((pt_signal * df_rtn)).sum(axis=1)
    return pt_return


















