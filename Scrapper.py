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
 
 
def make_correlation_matrix(combined_df, show_correlation_matrix):
    correlation_matrix = combined_df.corr(method='pearson')
    print('\n',"Corrélation moyenne: ",(correlation_matrix.mean()).mean(),'\n')
 
    if show_correlation_matrix == True:
        plt.matshow(correlation_matrix)
        plt.show()
 
 

 
def training_test_sets(data_actual,
                       data_big,
                       actual_timeframe,
                       big_timeframe,
                       small_timeframe,
                       number_of_periods_bebore_x,
                       number_of_periods_after_x_total,
                       train_test_ratio,
                       x_train_supervised,
                       x_test_supervised,
                       y_train_supervised,
                       y_test_supervised,
                       labels):

    for altcoin_1 in data_actual:
        print(data_actual[altcoin_1].head(20),'\n')
        total_lenght_big = len(data_big[altcoin_1].tolist())
        break

    ratio = big_timeframe/actual_timeframe
    number_periods_bebore_x = number_of_periods_bebore_x*big_timeframe/actual_timeframe
    number_periods_after_x = number_of_periods_after_x_total*big_timeframe/actual_timeframe
    
    global first_time

    if ratio == 1:
        add = 0
    if ratio == 4:
        add = 3
    if ratio == 8:
        add = 7

    mult =10
    counter = 0 
    for altcoin in data_actual:
        lol = data_actual[altcoin].tolist()

        if first_time ==True:
            for i in range(int(number_periods_bebore_x)+add, int(int(total_lenght_big*train_test_ratio)*ratio) - int(number_periods_after_x)): 
                x_train_supervised.append([((y/lol[i]-1)*mult) for y in lol[i+1-number_of_periods_bebore_x:i+1]]) 
                                y_train_supervised.append([((y/lol[i]-1)*mult) for y in lol[i+1:i+1+int(number_periods_after_x)]])
                labels.append([altcoin])
                counter +=1
        else:
            multiplier = int(actual_timeframe/small_timeframe)
            for i in range(int(number_periods_bebore_x)+add, int(int(total_lenght_big*train_test_ratio)*ratio) - int(number_periods_after_x)):
                for ii in range(multiplier):
                    try:
                        x_train_supervised[counter].extend([((y/lol[i]-1)*mult) for y in lol[i+1-number_of_periods_bebore_x:i+1]])
                    except:
                        pass
                    counter += 1
    
    print("Le nombre de données utilisées pour train le modèle supervisé: ", len(x_train_supervised),", avec %s collonnes" %(len(x_train_supervised[-1])))

    
    counter = 0 
    for altcoin in data_actual:
        lol = data_actual[altcoin].tolist()

        if first_time ==True:
            for i in range(int(int(total_lenght_big*train_test_ratio)*ratio)+add, int(int(total_lenght_big*train_test_ratio)*ratio)+int(int(total_lenght_big*(1-train_test_ratio))*ratio-int(number_periods_after_x))): ####Ici on peut ou non ajouter +1, on peut aussi diminuer le nombre de jours après x
                x_test_supervised.append([((y/lol[i]-1)*mult) for y in lol[i+1-number_of_periods_bebore_x:i+1]])
                y_test_supervised.append([((y/lol[i]-1)*mult) for y in lol[i+1:i+1+int(number_periods_after_x)]])
                
                counter +=1
        else:
            multiplier = int(actual_timeframe/small_timeframe)
            for i in range(int(int(total_lenght_big*train_test_ratio)*ratio)+add, int(int(total_lenght_big*train_test_ratio)*ratio)+int(int(total_lenght_big*(1-train_test_ratio))*ratio)):
                for ii in range(multiplier):
                    try:
                        x_test_supervised[counter].extend([((y/lol[i]-1)*mult) for y in lol[i+1-number_of_periods_bebore_x:i+1]])
                    except:
                        pass
                    counter += 1

    print("Le nombre de données utilisées pour test le modèle supervisé: ", len(x_test_supervised),", avec %s collonnes" %(len(x_test_supervised[-1])))
     
   
    first_time = False
    return x_train_supervised, x_test_supervised, y_train_supervised, y_test_supervised, labels

     



def calculate_outputs(y_train_supervised,
                      y_test_supervised):


    for row in range(len(y_train_supervised)):  
        y_train_supervised[row] = [sum(y_train_supervised[row])/len(y_train_supervised[row])]

    for row in range(len(y_test_supervised)):  
        y_test_supervised[row] = [sum(y_test_supervised[row])/len(y_test_supervised[row])]


    return y_train_supervised, y_test_supervised


    
#     Partie 2   
################################################# On définit les variables ##################################################
 
base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2016-02-17 00:00:00', '%Y-%m-%d %H:%M:%S')
end_date = datetime.now()
period_table = [900, 1800,7200] ##valid values are 300, 900, 1800, 7200, 14400, and 86400 (valeurs en secondes)
compute_correlation = False
show_correlation_matrix = True
show_period_division_graph = True
 
 
altcoins = ["ETH","XRP","LTC","XMR","LSK","STR","XEM","ETC","BCH","ZEC","BTS",
            "ZRX","STRAT","OMG","DGB","VTC","GAME","DCR","PPC",
            "REP","GNT","EMC2","FCT","MAID","SYS","ARDR","STEEM","CVC","VIA",
            "VRC","EXP","GAS","LBC","BURST","PASC","XCP","STORJ","GNO","NAV","CLAM",
            "POT","AMP","OMNI","BLK","XVC","RADS","NXC","GRC","FLO","BELA","BTM",
            "PINK","RIC","XBC","SBD","BCY","FLDC","HUC","NEOS"]
altcoins = ["ETH"]
 
 
 
#     Partie 3
################################################# On execute le code ###############################################
df_list = []
altcoins_list = []
for pediod in period_table:
     
    folder, min_lenght = choose_timeframe(pediod)
 
    altcoin_data = alcoin_extract_from_poloniex(altcoins)
 
    combined_df = merge_dfs_on_column(list(altcoin_data.values()), list(altcoin_data.keys()), 'close')

    combined_df = combined_df[:]['2017-02-18 00:00:00':'2018-02-01 00:00:00']
 
    df_list.append(combined_df)
 
    if compute_correlation == True:
        make_correlation_matrix(combined_df, show_correlation_matrix)
 
 

 
list_index = 0
total_list =[]
x_train_supervised, x_test_supervised,  = [], []
y_train_supervised, y_test_supervised,  = [], []
labels = []

first_time = True


number_of_periods_bebore_x = 60
for pediod in period_table:
 
 
##    lol = df_list[list_index]
##    variation_graph(lol)
 
    print("En train de traiter les chandelles de: %s sec" %(period_table[list_index]))
 
 
    combined_df_big, combined_df_actual = df_list[-1], df_list[list_index]

    
    x_train_supervised, x_test_supervised, y_train_supervised, y_test_supervised, labels = training_test_sets(data_actual = combined_df_actual,
                                                                                                      data_big = combined_df_big,
                                                                                                      actual_timeframe = period_table[list_index],
                                                                                                      big_timeframe = period_table[-1],
                                                                                                      small_timeframe = period_table[0],
                                                                                                      number_of_periods_bebore_x = number_of_periods_bebore_x,
                                                                                                      number_of_periods_after_x_total = 5,
                                                                                                      train_test_ratio = 0.8,
                                                                                                      x_train_supervised = x_train_supervised,
                                                                                                      x_test_supervised = x_test_supervised,
                                                                                                      y_train_supervised = y_train_supervised,
                                                                                                      y_test_supervised = y_test_supervised,
                                                                                                      labels = labels) 
    list_index+=1


    
y_train_supervised, y_test_supervised = calculate_outputs(y_train_supervised,
                                                          y_test_supervised)


print(len(x_train_supervised))
##import time
##plt.ion()
##try:
##    for row in range(0,len(x_train_supervised),1):
##        #for x in range(number_of_periods_bebore_x,number_of_periods_bebore_x*4,number_of_periods_bebore_x):
##        plt.plot(x_train_supervised[row][0:200]+[y_train_supervised[row][0]], label="15 min")
##        plt.plot(x_train_supervised[row][200:400], label="30 min")
##        plt.plot(x_train_supervised[row][400:600], label="2 h")
##        #plt.plot(x_test_supervised[row][x-number_of_periods_bebore_x:x], label=x)
##        plt.xlabel('Dates')
##        plt.ylabel('Prix')
##        plt.title(labels[row][0])
##        plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
##        plt.pause(0.01)
##        plt.clf()
##
##
##except KeyboardInterrupt:
##    pass
##plt.close()


