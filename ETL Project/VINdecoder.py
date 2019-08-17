#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from pprint import pprint
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import requests
import time


# In[2]:


url = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/5UXWX7C5*BA?format=json"


# In[28]:


car = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/WBAUP7C56CVP22994?format=json"


# In[29]:


autos = requests.get(car).json()
autos


# In[7]:


make = autos['Results'][6]['Value']
model = autos['Results'][8]['Value']
year = autos['Results'][9]['Value']
print(make)
print(model)
print(year)


# In[10]:


vehicle_file = "Resources/true_car_listings.csv"
vehicle_df = pd.read_csv(vehicle_file)
vehicle_df.head()


# In[17]:


url2 = "https://vpic.nhtsa.dot.gov/api/vehicles/decodevin/"
    


# In[18]:



query = f"{url2}5UXWX7C5*BA?format=json"


# In[19]:


test = requests.get(query).json()
test


# In[31]:


short_vehicle_df = vehicle_df[:10]
short_vehicle_df


# In[49]:


make = []


# In[50]:


model = []


# In[51]:


year = []


# In[52]:


for i in short_vehicle_df['Vin']:
    query = f"{url2}{i}?format=json"
    response = requests.get(query).json()
    
    make.append(response['Results'][6]['Value'])
    model.append(response['Results'][8]['Value'])
    year.append(response['Results'][9]['Value'])
                


# In[ ]:





# In[53]:


make


# In[54]:


model


# In[55]:


year


# In[56]:


new_vehicle_df = short_vehicle_df[['Price','City','State','Mileage','Vin']]
new_vehicle_df.head()


# In[57]:


new_vehicle_df['make'] = make
new_vehicle_df['model'] = model
new_vehicle_df['year'] = year


# In[58]:


new_vehicle_df.head()


# In[59]:


new_vehicle_df.to_csv("VINdecoded_true_car_listings.csv", index = False)


# In[ ]:




