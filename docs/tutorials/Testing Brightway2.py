#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#To install bw2, use https://2.docs.brightway.dev/installation.html


# In[1]:


#remember to launch this from the command line in the "mytestenv" environment
#because currently bw2 is only installed in that environment?
import os
import numpy as np
import pandas as pd
import brightway2 as bw2


# In[7]:


bw2.projects.create_project('bw2-seminar-tutorial')
bw2.projects.set_current('bw2-seminar-tutorial')
bw2.projects.current #shows current project
#also "see what projects you have on your computer by running list(bw.projects)"


# In[11]:


bw2.projects.dir
bw2.bw2setup() # need this to create pathways, mapping, and methods - it creates biosphere3


# # #activities in the database

# In[29]:


bw2.databases
mybio = bw2.Database('biosphere3')
#type(mybio)
#len(mybio)
random = mybio.random() #returns a random "activity" from the database, these can be assigned to a variable for use
#LCA language for here; an "activity" is an elementary flow in LCA world. 
#here activities are linked by edges (exchanges)
type(random)
random.as_dict() #this shows what is contained in the activity


# In[33]:


key = ('biosphere3', random['code']) #creates a tuple to pass to the get function
bw2.get_activity(key) #the get function takes in a sinple argument in the form of the tuple of a database name and it's code
type(random.key) #this is the better way to get the key of a a particular activity


# In[39]:


#How to Search for an item in the database
bw2.Database('biosphere3').search('silver') #returns all with that title
#filter down using
bw2.Database('biosphere3').search('carbon dioxide', filter={'categories':'urban', 'name':'fossil'})
#can use forloop iteration to search as well


# # #methods

# In[ ]:




