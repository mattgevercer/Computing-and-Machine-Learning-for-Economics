#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 12:39:31 2021

@author: mattgevercer
"""
# c = 'EG.ELC.ACCS.RU.ZS'
# y = 2010

def worldbankimport(code, year):
    from bs4 import BeautifulSoup
    import urllib.request as url
    import pandas as pd
    url1 = 'https://api.worldbank.org/v2/country/all/indicator/' + code +'?date='+ str(year)
    req = url.Request(url1)
    xml = url.urlopen(req)
    soup = BeautifulSoup(xml,"xml")
    tag = soup.contents[0]
    pages = int(tag.attrs['pages'])
    data = soup.find_all("data")[0]
    #create df for page 1 
    xmldf = pd.DataFrame()
    for i in range(1,len(data),2): #interate through all odd-indexed rows
        row = data.contents[i]
        cells = row.contents[1:len(row.contents):2]
        rowdict = {}
        for j in range(len(cells)):
            rowdict[cells[j].name] = cells[j].string
        xmldf=xmldf.append(rowdict,ignore_index=True)
    
    for i in range(2, pages+1):
        url2 = url1+ '&page=' + str(i)
        req2 = url.Request(url2)
        xml2 = url.urlopen(req2)
        soup2 = BeautifulSoup(xml2,"xml")
        data2 = soup2.find_all("data")[0]
        for i in range(1,len(data2),2): #interate through all odd-indexed rows
            row = data2.contents[i]
            cells = row.contents[1:len(row.contents):2]
            rowdict = {}
            for j in range(len(cells)):
                rowdict[cells[j].name] = cells[j].string
            xmldf=xmldf.append(rowdict,ignore_index=True)
    return xmldf
    
# v = worldbankimport(c,y)



