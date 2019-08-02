#!/usr/bin/env python
# coding: utf-8

# In[3]:


# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import StandardScaler
from dateutil import rrule
import datetime
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
import numpy as np
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import shutil
import datetime as dt
from IPython.display import display, clear_output
import geopy.distance as distance
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


print(dt.datetime.now()," Start Process")


# In[9]:


# open files of interests and append together
df_main = pd.read_csv('/scratch/skp454/Trajectory/TaxiDataSet/data/20190627_TaxiData.csv')
df_main.head()


# In[10]:
# Trim data based on Lat Lon
print('LAT', df_main['LAT'].min(), df_main['LAT'].max())
print('LON', df_main['LON'].min(), df_main['LON'].max())
print(len(df_main))

df_main = df_main[(df_main['LAT']>35) * (df_main['LAT']<45)]
df_main = df_main[(df_main['LON']>110) * (df_main['LON']<125)]

print('LAT', df_main['LAT'].min(), df_main['LAT'].max())
print('LON', df_main['LON'].min(), df_main['LON'].max())
print(len(df_main))

#number of active taxi
VN=len(df_main.TaxiID.unique());
print("No.of Active Vessels", VN)


# In[11]:


print(dt.datetime.now()," Change to DateTime")


# In[12]:


# convert to datetime
df_main['BaseDateTime'] =pd.to_datetime(df_main.BaseDateTime)

# sort df_main
df_main = df_main.sort_values(by=['TaxiID','BaseDateTime'])

#reset_index
df_main.reset_index(inplace=True, drop=True)


# In[13]:


print(dt.datetime.now()," Creating Trips")


# In[14]:


# function to calculate distance between consecutive points
def calcDist(lat, lon):
    df_dist = pd.DataFrame(np.array([lat[:-1],lon[:-1],lat[1:],lon[1:]]).T)
    df_dist['Dist'] = df_dist.apply(lambda row: distance.geodesic((row[0],row[1]),(row[2],row[3])).km, axis=1)
    return df_dist['Dist']


# In[17]:


# create time_Diff
t=np.array(df_main.BaseDateTime)
I=list((t[1:]-t[:-1])/np.timedelta64(1, 's'))
I=[0] + I
df_main['TimeDiff'] = I

# MMSI Diff
m=np.array(df_main.TaxiID)
M=list(m[1:]-m[:-1])
M=[1] + M
df_main['IdDiff'] = M

# Distance diff
df_main['Dist'] = [0] + list(calcDist(df_main['LAT'],df_main['LON']))

#Speed
df_main['Speed'] = (df_main['Dist']*3600)/df_main['TimeDiff']
df_main['Speed'].fillna(0, inplace =True)

#Actual time Diff
df_main['IdDiff'] = df_main['IdDiff']==0
df_main['TimeDiff'] = df_main['TimeDiff'] * df_main['IdDiff']
df_main['Dist'] = df_main['Dist'] * df_main['IdDiff']
df_main['Speed'] = df_main['Speed'] * df_main['IdDiff']

# drop unneccessary zero time diff
df_main.drop(index = df_main[(df_main['TimeDiff']==0)*(df_main['IdDiff']==True)].index, inplace =True)

#reset_index
df_main.reset_index(inplace=True, drop=True)

# stationarity
df_main['Stationary'] = df_main['Speed']<0.03

# stationarity id
df_main['trip_id'] = df_main['Stationary'].cumsum()

# view data
df_main.head()


# In[18]:


# Save data
df_main.to_csv('/scratch/skp454/Trajectory/TaxiDataSet/data/20190627_TaxiTripMainData.csv', index = False)


# In[19]:


print(dt.datetime.now()," Creating Trips Statistics")


# In[20]:


# calculate dispacement
df_displacement = pd.DataFrame()
df_displacement['trip_id'] = list(df_main[df_main['Stationary'] == 1].trip_id)
df_displacement['Start'] = list(df_main[df_main['Stationary'] == 1].index)
df_displacement['End'] = list(df_main[df_main['Stationary'] == 1].index)[1:] + [len(df_main)]
df_displacement['End'] = df_displacement['End'] - 1
df_displacement['displacement'] = df_displacement.apply(lambda row:distance.geodesic                                                        ((df_main.loc[row['Start'],'LAT'],
                                                          df_main.loc[row['Start'],'LON']),
                                                         (df_main.loc[row['End'],'LAT'],
                                                          df_main.loc[row['End'],'LON'])).km, axis =1)
# Calculate Distance Time and Speed for Trips
df_main = df_main[df_main['Stationary'] == False]
df_main['Count'] = 1
df_trip = pd.DataFrame(df_main.groupby(['trip_id','TaxiID'], as_index=False)['Dist','TimeDiff','Count'].sum())
del df_main['Count']
df_trip['Speed'] = df_trip['Dist']*3600/df_trip['TimeDiff']

# Merge with trip data
df_trip = df_trip.merge(df_displacement[['trip_id','displacement']], on ='trip_id', how='inner')

# Save trip data
df_trip.to_csv('/scratch/skp454/Trajectory/TaxiDataSet/data/20190621_TaxiTripStatsData.csv', index = False)

