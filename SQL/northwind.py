#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 08:49:04 2021

@author: mattgevercer
"""
import sqlite3
import pandas as pd

con = sqlite3.connect("northwind.db") 
con.text_factory = lambda b: b.decode(errors = 'ignore') 

#pd.read_sql_query("select name from sqlite_master where type='table'",con)

d1 = pd.read_sql_query("select * \
                  from Orders \
                  where ShipCountry = 'USA'",con)
                  
# d2 = pd.read_sql_query("select distinct ShipCountry \
#                        from Orders",con)
                       
d2 = pd.read_sql_query("select distinct Country \
                      from Customer",con)

d3 = pd.read_sql_query("select Country, count(Id) as NumCustomer \
                      from Customer\
                      group by Country\
                      having NumCustomer >1\
                      order by NumCustomer desc",con)
                      
d4 = pd.read_sql_query("select Orders.Id\
                       from Customer join Orders\
                       on Orders.CustomerId = Customer.Id\
                       where Orders.ShipCountry <> Customer.Country",con)
                       
d5 = pd.read_sql_query("select OrderId, sum((1- Discount)*UnitPrice*Quantity) as revenue\
                       from OrderDetail\
                       group by OrderId",con)
                       
d6 = pd.read_sql_query("select Orders.Id, OrderDate, sum((1- Discount)*UnitPrice*Quantity) as revenue\
                       from OrderDetail join Orders\
                       on Orders.Id = OrderDetail.OrderId\
                       join Customer\
                       on Orders.CustomerId = Customer.Id\
                       group by Orders.Id\
                       having Customer.Country = 'USA'",con)

d7 = pd.read_sql_query("select distinct Customer.CompanyName\
                       from Customer join Orders\
                       on Orders.CustomerId = Customer.Id\
                       where ShipCity = 'Eugene'",con)
                       
# d8 = pd.read_sql_query("select Customer.CompanyName, ShipCity\
#                         from Customer join Orders\
#                         on Orders.CustomerId = Customer.Id\
#                         where ShipCity = 'Eugene'\
#                         order by Customer.CompanyName",con)

d8 = pd.read_sql_query("select Customer.CompanyName\
                       from Customer join Orders\
                       on Orders.CustomerId = Customer.Id\
                       where ShipCity = 'Eugene'\
                       group by Customer.CompanyName\
                       having count(Customer.CompanyName)>1",con)
                       
def orderlookup(city,country):
    import sqlite3
    import pandas as pd
    con = sqlite3.connect("northwind.db") 
    con.text_factory = lambda b: b.decode(errors = 'ignore')
    city = "'"+city+"'"
    country = "'"+country+"'"
    data = pd.read_sql_query("select *\
                             from Orders\
                             where ShipCity =" + city +\
                             " and ShipCountry =" +country,con)
    return data


