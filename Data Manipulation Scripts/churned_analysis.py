# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 20:36:06 2018

@author: beena
"""
import pandas as pd


segment = pd.read_csv("RFM_FINAL_SCORE.csv")
transaction = pd.read_csv("transaction_data.csv")
casual = pd.read_csv("causal_data.csv")
product = pd.read_csv("product.csv")


merge_1 = pd.merge(transaction,segment,left_on=['household_key'], right_on=['Household'],how="left")

master= pd.merge(merge_1,product,left_on=['PRODUCT_ID'], right_on=['PRODUCT_ID'],how="left")



### subsetting master with almost churned customers

Almost_Lost=master[master['Segment']=='Almost Lost']
Big_Spenders=master[(master['Segment']=='Big Spenders')]
L_C_C=master[(master['Segment']=='Lost Cheap Customers')]


### Brands that Almost Lost customers are interested in

Brands_AL=Almost_Lost.groupby('COMMODITY_DESC').agg({'household_key_x':'nunique'}).reset_index()

Brands_AL.sort_values(by=['household_key_x'],ascending=False)


###Brands that Big spenders are interested in
Brands_bs=Big_Spenders.groupby('COMMODITY_DESC').agg({'household_key_x':'nunique'}).reset_index()

Brands_bs.sort_values(by=['household_key_x'],ascending=False)


###Brands that L C C WERE interested in
Brands_lcc=L_C_C.groupby('COMMODITY_DESC').agg({'household_key_x':'nunique'}).reset_index()

Brands_lcc.sort_values(by=['household_key_x'],ascending=False)


###Store IDs shopped across segments###############

STORE_AL=Almost_Lost.groupby('STORE_ID').agg({'household_key_x':'nunique'}).reset_index()

STORE_AL.sort_values(by=['household_key_x'],ascending=False)

STORE_AL.columns=['STORE_ID','Almost Churned']


###Brands that Big spenders are interested in
STORE_bs=Big_Spenders.groupby('STORE_ID').agg({'household_key_x':'nunique'}).reset_index()

STORE_bs.sort_values(by=['household_key_x'],ascending=False)


STORE_bs.columns=['STORE_ID','Big_Spenders']

###Brands that L C C WERE interested in
STORE_lcc=L_C_C.groupby('STORE_ID').agg({'household_key_x':'nunique'}).reset_index()

STORE_lcc.sort_values(by=['household_key_x'],ascending=False)


#### Join store data for lost customers and big spenders

merge_2 = pd.merge(STORE_bs,STORE_AL,left_on=['STORE_ID'], right_on=['STORE_ID'],how="outer")



merge_2.to_csv('Store_Analysis.csv')



