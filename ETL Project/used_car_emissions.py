#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sqlalchemy import create_engine


# In[6]:


#Import the CSV file and extract CSV it into DataFrame
vehicle_file = "Resources/vehicles-2.csv"
vehicle_df = pd.read_csv(vehicle_file)
vehicle_df.head()


# In[15]:


#Import the CSV file and extract CSV it into DataFrame
used_car_file = "Resources/true_car_listings.csv"
used_car_df = pd.read_csv(used_car_file)
used_car_df.head()


# In[7]:


vehicle_col = ['make', 'model', 'year','co2TailpipeGpm','fuelType', 'fuelType1']
vehicle_transformation_df = vehicle_df[vehicle_col]
vehicle_transformation_df.head()


# In[8]:


vehicle_transformed = vehicle_transformation_df.rename(columns={
   'co2TailpipeGpm': 'co2_tailpipe_gpm',
    'fuelType': 'fuel_type',
    'fuelType1':'fuel_type1'
})
vehicle_transformed.head()


# In[9]:


vehicle_transformed['id'] = vehicle_transformed.index
vehicle_transformed.head()


# In[17]:


used_car_col = ['Year', 'Make', 'Model','Price','Mileage','City','State','Vin']
used_car_transformation_df = used_car_df[used_car_col]


# In[18]:


used_car_transformed = used_car_transformation_df.rename(columns={
    'Year': 'year',
    'Make': 'make',
    'Model': 'model',
    'Price':'price',
    'Mileage':'mileage',
    'City':'city',
    'State':'state',
    'Vin':'vin'
})


# In[19]:


used_car_transformed.head()


# In[20]:


used_car_transformed=used_car_transformed.reset_index(drop=False)
used_car_transformed.head()


# In[22]:


used_car_transformed2 = used_car_transformed.rename(columns={'index': 'id'})
used_car_transformed2.head()


# In[11]:


rds_connection_string = "postgres:NIM2006@localhost:5432/automobile_db"
engine = create_engine(f'postgresql://{rds_connection_string}')


# In[13]:


engine.table_names()


# In[26]:


vehicle_transformed.to_sql(name='emission', con=engine, if_exists='append', index=False)


# In[27]:


used_car_transformed2.to_sql(name='used_car', con=engine, if_exists='append', index=False)


# In[28]:


get_ipython().system('jupyter nbconvert --to script used_car_emissions_copy.ipynb')


# In[ ]:




