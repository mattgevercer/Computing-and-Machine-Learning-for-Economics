#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 11:27:05 2021

@author: mattgevercer
"""
import pandas as pd
import numpy as np

d = pd.read_fwf('https://wilson.engr.wisc.edu/rsfc/history/howell/cf2010gms.txt') 
#date, awayteam, awayscore, hometeam, homescore, location
def ncaaimport(y):
    """
    Parameters
    ----------
    y : Year of type int

    Returns: a dataframe of NCAA win-loss data

    """  
    year = str(y)
    url1 = 'https://wilson.engr.wisc.edu/rsfc/history/howell/cf'
    url2 = 'gms.txt'
    url_full = url1 + year + url2 #create full url 
    d = pd.read_fwf(url_full,
                    widths = [(10),(28),(4),(28),(4),(28),(10)],
                    header = None).iloc[:, [0,1,2,3,4,5]] #read in the data from txt file
    d.columns = ['date', 'awayteam', 'awayscore', 'hometeam', 
                 'homescore', 'location']
 
    away = d.groupby(#count number of away games per team
        'awayteam').agg({'awayteam':['size']}
                        ).reset_index()
    away.columns = away.columns.map(''.join)                    
    home = d.groupby(# count home games per team
        'hometeam').agg({'hometeam':['size']}
                        ).reset_index()
    home.columns = home.columns.map(''.join)
    #merge home and away
    merged = pd.merge(away, home, how='outer', 
                      left_on='awayteam', right_on='hometeam'
                      ).fillna(0)
    #create array of teams with fewer than 6 games played
    T_6 = merged[merged['awayteamsize']+merged['hometeamsize']<6]
    T_6 = np.concatenate((T_6['awayteam'].values[T_6['awayteam'].values.nonzero()],
                         T_6['hometeam'].values[T_6['hometeam'].values.nonzero()])
        )
    # drop teams with fewer than 6 games from orig. data
    d_6 = d[~d['awayteam'].isin(T_6)]
    d_6 = d_6[~d_6['hometeam'].isin(T_6)]
    #drop ties
    d_6 = d_6[d_6['homescore']!=d_6['awayscore']]
    #add columns for homewins and away wins
    d_6['homewin'] = d_6['homescore']>d_6['awayscore']
    d_6['awaywin'] = d_6['awayscore']>d_6['homescore']
    
    #count number of away games per team and away wins
    away2 = d_6.groupby(
        'awayteam').agg({'awayteam':['size'],'awaywin':['sum']}
                        ).reset_index()
    away2.columns = away2.columns.map(''.join)                    
    # count home games per team and home wins 
    home2 = d_6.groupby(
        'hometeam').agg({'hometeam':['size'], 'homewin':['sum']}
                        ).reset_index()
    home2.columns = home2.columns.map(''.join)
    merged2 = pd.DataFrame({
        'team':away2['awayteam'],
        'wins': away2['awaywinsum']+home2['homewinsum'],
        'losses': home2['hometeamsize']+away2['awayteamsize']-away2['awaywinsum']-home2['homewinsum']
        })
    # make hash table with team as index and number as value 
    t_hash = pd.Series(list(range(len(merged2['team']))),merged2['team'])
    #add ID of the away team to full data
    d_6['away_id']= t_hash[d_6['awayteam']].values
    #add ID of the home team to full data
    d_6['home_id']= t_hash[d_6['hometeam']].values  #create data frame of teams and their opps at away games
    opps1 = d_6.groupby(["awayteam"]).agg({"home_id": list})
    #create data frame of teams and their opps at home games
    opps2 = d_6.groupby(["hometeam"]).agg({"away_id": list})
    f_opps = [[] for i in range(len(merged2))]
    for i in range(len(merged2)):#merged2['team']:
        if merged2['team'][i] in opps1.index.values:
            f_opps[i] = opps1.loc[merged2['team'][i]]['home_id'] + f_opps[i]
        if merged2['team'][i] in opps2.index.values:
            f_opps[i] = opps2.loc[merged2['team'][i]]['away_id'] + f_opps[i]
    #combine home opps and away opps for each team        
    merged2['opponents'] = f_opps 
    return merged2
