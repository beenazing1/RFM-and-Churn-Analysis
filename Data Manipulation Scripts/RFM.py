import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns

file = pd.read_csv("data_segment_v2.csv")

#file.columns

### Recency Frequency Model - Household Engagement Score - need to fit in the recency variable - in this
### to better target coupons - see which coupons are being redeemed 
### by the top customers
### correlations between products 


#### Hypothesis:

### 1) Customers who belong to the high RFM sector are most loyal
### 2) Increasing the total coupon discount and the loyalty discount increases sales  - regression model
### 3) Do Coupons lead to repeat purchases - once the coupon has been redeemed  
### 4) analyse dollar sales and unit sales before and after coupon usage  - dont need househoold level data
### 5) ### how does coupon usage affect sales/ transaction price 

### 6) regress coupon usage with sales/ quantity - increasing coupon usage decreases sales


### higher loyalty discount by people high in RFM
### Do people purchase more with loyalty of not?



transaction = pd.read_csv("transaction_data.csv")
#transaction['SALES_VALUE'] 


##### Household group by
RFM= transaction.groupby('household_key').agg({'DAY':'max','BASKET_ID':'nunique','SALES_VALUE':'sum'}).reset_index()


RFM.columns=["Household","Recency","Frequency","Monetary"]


## recency small quantile is good
## freq monetary large quantile is good  -- hence 2 separate classes

def RClass(x,p,d):
    if x <= d[p][0.25]:
        return 1
    elif x <= d[p][0.50]:
        return 2
    elif x <= d[p][0.75]: 
        return 3
    else:
        return 4
    
# Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
def FMClass(x,p,d):
    if x <= d[p][0.25]:
        return 4
    elif x <= d[p][0.50]:
        return 3
    elif x <= d[p][0.75]: 
        return 2
    else:
        return 1


### create quantiles for segmentation

quantiles=RFM.quantile([0.25,0.5,0.75])
quantiles = quantiles.to_dict()

## check distribution of recency

sns.distplot(RFM['Recency'])

a=RFM['Recency'].max()

#### less than 2 months is counted as not active
b=a-60

### less than 4 months  - danger of churn

c=b-60


### give customer a cutoff of 2 months
quantiles['Recency'][0.25]=c
quantiles['Recency'][0.5]=b
quantiles['Recency'][0.75]=a



RFM['R_score']=RFM['Recency'].apply(RClass,args=('Recency',quantiles))
RFM['F_score']=RFM['Frequency'].apply(FMClass,args=('Frequency',quantiles))
RFM['M_score']=RFM['Monetary'].apply(FMClass,args=('Monetary',quantiles))

### Group by score and count
RFM=pd.DataFrame(RFM)
# =============================================================================
# RFM_group = RFM.groupby(['R_score','F_score','M_score']).count().reset_index()
# 
# RFM_group=RFM_group.rename(columns={'Household':'Count'})
# 
# RFM_group=RFM_group.drop(RFM_group.columns[[4,5,6]],axis=1)
# 
# 
# =============================================================================
#RFM_group.to_csv('RFM.csv')

#2500 household types
#file.household_key.value_counts()

coupon_redeem = pd.read_csv("coupon_redempt.csv")
coupon_desc = pd.read_csv("campaign_desc.csv")


coupons = pd.merge(RFM,coupon_redeem,left_on=['Household'], right_on=['household_key'])

coupons.to_csv('Coupons.csv')
