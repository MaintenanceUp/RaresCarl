import os
import numpy as np
import pandas as pd
import pickle
import quandl
from datetime import datetime
import matplotlib.pyplot as plt
import math
import random
from datetime import datetime, date, timedelta
import stockstats
from stockstats import StockDataFrame

 
#     Partie 1
################################################################## On définit les fonctions ########################################
 
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
    try:        
        f = open(cache_path, 'rb')
        df = pickle.load(f)   
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df
 
def get_crypto_data(poloniex_pair):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    data_df = get_json_data(json_url, folder+poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df
 
 
def merge_dfs_on_column(dataframes, labels, col):
    '''Merge a single column of each dataframe into a new combined dataframe'''
    series_dict = {}
    altcoins_list = []
    for index in range(len(dataframes)):
        if len(dataframes[index]["close"]) > min_lenght:
            series_dict[labels[index]] = dataframes[index][col]
            altcoins_list.extend([labels[index]])
         
    return pd.DataFrame(series_dict)
  
  
def choose_timeframe(pediod):
    if pediod == 300:
        folder = "5_min/"
        min_lenght = 210000
 
    if pediod == 900:
        folder = "15_min/"
        min_lenght = 70000
 
    if pediod == 1800:
        folder = "30_min/"
        min_lenght = 35000
 
    if pediod == 7200:
        folder = "2_h/"
        min_lenght = 8750
     
    if pediod == 14400:
        folder = "4_h/"
        min_lenght = 4375
         
    if pediod == 86400:
        folder = "1_j/"
        min_lenght = 729
 
    return folder, min_lenght
 
def alcoin_extract_from_poloniex(altcoins):
    altcoin_data = {}
    for altcoin in altcoins:
        coinpair = 'BTC_{}'.format(altcoin)
        crypto_price_df = get_crypto_data(coinpair)
        altcoin_data[altcoin] = crypto_price_df
 
    return altcoin_data
 
def calculate_indicators(altcoin_data):
    stock = StockDataFrame.retype(altcoin_data["ETH"])
    dictionnary = {}


    #Moving average
    dictionnary["Ema_3"] = stock['open_3_ema'] #comme le prix, inconstant
    dictionnary["Ema_5"] = stock['open_5_ema'] #comme le prix, inconstant
    dictionnary["Ema_8"] = stock['open_8_ema'] #comme le prix, inconstant
    dictionnary["Ema_10"] = stock['open_10_ema'] #comme le prix, inconstant
    dictionnary["Ema_12"] = stock['open_12_ema'] #comme le prix, inconstant
    dictionnary["Ema_15"] = stock['open_15_ema'] #comme le prix, inconstant
    dictionnary["Ema_30"] = stock['open_30_ema'] #comme le prix, inconstant
    dictionnary["Ema_35"] = stock['open_35_ema'] #comme le prix, inconstant
    dictionnary["Ema_40"] = stock['open_40_ema'] #comme le prix, inconstant
    dictionnary["Ema_45"] = stock['open_45_ema'] #comme le prix, inconstant
    dictionnary["Ema_50"] = stock['open_50_ema'] #comme le prix, inconstant
    dictionnary["Ema_60"] = stock['open_60_ema'] #comme le prix, inconstant
    dictionnary["Ema_100"] = stock['open_100_ema'] #comme le prix, inconstant
    dictionnary["Ema_200"] = stock['open_200_ema'] #comme le prix, inconstant
    ##
    ###MACD
    dictionnary["MACD"] = stock['macd'] # -0.003 à 0.003 inconstant
    dictionnary["MACD"] = stock['macds'] # -0.004 à 0.003 inconstant
    dictionnary["MACD"] = stock['macdh'] # -0.003 à 0.003 inconstant

    plt.plot(altcoin_data["ETH"]["open"])
    ###Bollinger bands
    dictionnary["bollinger"] = stock['boll'] #comme le prix, inconstant
    dictionnary["bollinger_up"] = stock['boll_ub'] #comme le prix, inconstant
    dictionnary["bollinger_low"] = stock['boll_lb'] #comme le prix, inconstant



    #RSI
    dictionnary["rsi_6"] = stock['rsi_6'] #0 à 100, constant
    dictionnary["rsi_12"] = stock['rsi_12']  #0 à 100, constant

    #WR
    dictionnary["wr_10"] = stock['wr_10'] #0 à 100, constant
    dictionnary["wr_6"] = stock['wr_6'] #0 à 100, constant

    #CCI
    dictionnary["cci_14"] = stock['cci'] #-600 à 600, constant
    dictionnary["cci_20"] = stock['cci_20']  #-600 à 600, constant

    # DMA, difference of 10 and 50 moving average
    dictionnary["dms"] = stock['dma'] #-0.015 à 0.015, inconstant

    # +DI, default to 14 days
    dictionnary['pdi']= stock['pdi'] # 0 à 100, constant
    # -DI, default to 14 days
    dictionnary['mdi']=stock['mdi'] # 0 à 100, constant
    # DX, default to 14 days of +DI and -DI
    dictionnary['dx']=stock['dx'] # 0 à 100, constant
    # ADX, 6 days SMA of DX, same as stock['dx_6_ema']
    dictionnary['adx']=stock['adx'] # 0 à 100, constant
    # ADXR, 6 days SMA of ADX, same as stock['adx_6_ema']
    dictionnary['adxr']=stock['adxr'] # 0 à 100, constant

    # TRIX, default to 12 days
    dictionnary['trix'] = stock['trix'] #-1 à 1
    ### MATRIX is the simple moving average of TRIX
    dictionnary['trix_9_sma'] = stock['trix_9_sma'] #-1 à 1

    # VR, default to 26 days
    dictionnary['vr'] = stock['vr'] #0 à3500
    # MAVR is the simple moving average of VR
    dictionnary['vr_6_sma'] = stock['vr_6_sma'] #0 à 1500

    # CR indicator, including 5, 10, 20 days moving average
    dictionnary['cr'] = stock['cr'] #0 à 500
    dictionnary['cr-ma1'] = stock['cr-ma1'] #0 à 500
    dictionnary['cr-ma2'] = stock['cr-ma2'] #0 à 500
    dictionnary['cr-ma3'] = stock['cr-ma3'] #0 à 500


    # KDJ, default to 9 days
    dictionnary['kdjk'] = stock['kdjk'] #-20 à 120
    dictionnary['kdjd'] = stock['kdjd'] #-20 à 120
    dictionnary['kdjj'] = stock['kdjj'] #-20 à 120

    dictionnary = pd.DataFrame(dictionnary)


    for name in dictionnary:
        plt.plot(dictionnary[name], label = name)
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.show()

    return dictionnary
    
#     Partie 2   
################################################# On définit les variables ##################################################
 
base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2016-02-17 00:00:00', '%Y-%m-%d %H:%M:%S')
end_date = datetime.now()
pediod = 900 ##valid values are 300, 900, 1800, 7200, 14400, and 86400 (valeurs en secondes)
compute_correlation = False
show_correlation_matrix = True
 
 
altcoins = ["ETH","XRP","LTC","XMR","LSK","STR","XEM","ETC","BCH","ZEC","BTS",
            "ZRX","STRAT","OMG","DGB","VTC","GAME","DCR","PPC",
            "REP","GNT","EMC2","FCT","MAID","SYS","ARDR","STEEM","CVC","VIA",
            "VRC","EXP","GAS","LBC","BURST","PASC","XCP","STORJ","GNO","NAV","CLAM",
            "POT","AMP","OMNI","BLK","XVC","RADS","NXC","GRC","FLO","BELA","BTM",
            "PINK","RIC","XBC","SBD","BCY","FLDC","HUC","NEOS"]
altcoins = ["ETH"]
 
 
 
#     Partie 3
################################################# On execute le code ###############################################
folder, min_lenght = choose_timeframe(pediod)
altcoin_data = alcoin_extract_from_poloniex(altcoins)
combined_df = calculate_indicators(altcoin_data)
combined_df = combined_df[:]['2016-02-18 00:00:00':'2018-02-01 00:00:00']
print(combined_df)


