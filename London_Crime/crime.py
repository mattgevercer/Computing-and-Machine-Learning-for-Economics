#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 10:43:47 2021

@author: mattgevercer
"""
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

fulldata = pd.read_csv("london_crime.csv")
fulldata['crimerate'] = fulldata['crime']/fulldata['population']
fulldata['policerate'] = fulldata['police']/fulldata['population']
fulldata["lcrime"]=np.log(fulldata.crimerate)
fulldata["lpolice"]=np.log(fulldata.policerate)
fulldata["lemp"]=np.log(fulldata.emp)
fulldata["lun"]=np.log(fulldata.un)
fulldata["lymale"]=np.log(fulldata.ymale)
fulldata["lwhite"]=np.log(fulldata.white)

model1=smf.ols("lcrime ~  lpolice + lemp + lun + lymale + lwhite",
               data=fulldata).fit()

new = fulldata.sort_values(['week','borough'])
new_diff = new.values[1664:3328,11:17]-new.values[0:1664,11:17]
diffdata =pd.DataFrame(new_diff)
diffdata.columns = ["dlcrime","dlpolice","dlemp","dlun","dlymale","dlwhite"]

model2=smf.ols("dlcrime ~ dlpolice + dlemp + dlun + dlymale +dlwhite",
               data=diffdata).fit()

year2 = new.values[1664:3328,0]
bor = new.values[1664:3328,8]

diffdata['sixweeks']= ( (year2 > 79) & (year2 <86))
treat = np.array(
    (bor ==1) | (bor==2) | (bor ==3) | (bor==6) | (bor==14)
    )

diffdata['sixweeks_treat'] = diffdata['sixweeks']&treat

diffdata['sixweeks_treat'] = diffdata['sixweeks_treat'].replace({True:1,False:0})
diffdata['sixweeks'] = diffdata['sixweeks'].replace({True:1,False:0})

model3 = smf.ols("dlcrime ~ sixweeks + sixweeks_treat + dlemp + dlun + dlymale +dlwhite",
                 data=diffdata).fit()
