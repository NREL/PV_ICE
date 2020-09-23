#!/usr/bin/env python
# coding: utf-8

# In[4]:


import CEMFC
#file = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
#fileglass = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_glass.csv'


# In[5]:


r1 = CEMFC.Simulation(name='Simulation1')


# In[6]:


r1.createScenario(name='standard')


# In[7]:


r1.scenario['standard'].addMaterial('glass') #, fileglass )


# In[10]:


r1.createScenario(name='NEVERRecycle')


# In[11]:


r1.scenario['NEVERRecycle'].addMaterial('glass')


# In[12]:


r1


# In[13]:


r1.__dict__


# In[14]:


r1.scenario['standard']


# In[17]:


r1.scenario['standard'].__dict__


# In[18]:


r1.scenario['standard'].material


# In[21]:


r1.scenario['standard'].material['glass'].__dict__


# In[2]:


r1.scenario['standard'].material.keys()


# In[22]:


r1.scenario['standard'].addMaterial('silicon')


# In[24]:


r1.scenario['standard'].material


# In[25]:


r1.scenario['standard'].material.keys()


# In[ ]:


r1.calculateMassFlow()


# In[ ]:


r1.plotMaterial(glass, Waste)


# In[ ]:





# In[3]:


for key in r1.scenario['standard'].material:
    print (key)


# In[15]:


for scenario in r1.scenario:
    print(scenario)
    for key1 in r1.scenario['standard'].material:
        print (key1)


# In[6]:


r1.scenario['standard'].material['glass'].__dict__


# In[7]:


r1.scenario['standard'].__dict__


# In[ ]:



r1.__dict__
r1.scenario['standard']
r1.scenario['standard'].__dict__
r1.scenario['standard'].material['glass']

foo = ScenarioObj('test')        
foo.__dict__
foo.set_sceneario_baseline('ideal', file)
foo.__dict__
foo.set_sceneario_baseline('decadent', file)

foo.module['ideal']['data']

foo.set_sceneario_baseline('decadent', file)



file = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
foo = ScenarioObj('test')        
foo.__dict__
foo.set_sceneario_baseline('ideal', file)
foo.__dict__
foo.set_sceneario_baseline('decadent', file)

foo.module['ideal']['data']

foo.set_sceneario_baseline('decadent', file)


# In[ ]:


class Simulation:
    def __init__(self):
        self.name='now'
        self.scenario={}
  
    def createScenario(self, name):
        self.scenario[name] = Scenario(name)


# In[ ]:


class Scenario:
    def __init__(self, name):
        self.name = name
        self.material={}

    def printName(self):
        print("My Scenario name is " + self.name)
        
    def addMaterial(self, materialname):
        self.material[materialname] = Material(materialname)


# In[ ]:


class Material:
    def __init__(self, name):
        self.name = name

    def printName(self):
        print("My Material name is " + self.name)


# In[ ]:


r1 = Simulation()
r1.createScenario('Prism')
r1.scenario['Prism'].addMaterial("glass")


# In[ ]:


r1.createScenario('meowmeow')


# In[ ]:


r1.__dict__


# In[ ]:


r1.scenario


# In[ ]:


r1.scenario.keys()


# In[ ]:


r1.scenario['Prism']


# In[ ]:


r1.scenario['Prism'].__dict__


# In[ ]:


r1.scenario['Prism'].name


# In[ ]:


r1.scenario['Prism'].printName()


# In[ ]:


r1.scenario['Prism'].material


# In[ ]:


r1.scenario['Prism'].material['glass']


# In[ ]:


r1.scenario['Prism'].material['glass'].__dict__


# In[ ]:


r1.scenario['Prism'].material['glass'].printName()


# # 

# In[ ]:


r1 = Simulation()
r2 = Module('Prism')


# In[ ]:


r1.module_owned = r2


# In[ ]:


r1.__dict__


# In[ ]:


r1.Scenario.name='hello'


# In[ ]:


r1.Scenario.calculateCI()


# In[ ]:


r1.name = "Tom"
r1.color = "red"
r1.weight = 30


# In[ ]:


r1.calculateCI()


# In[ ]:





# In[ ]:


for year, row in df.iterrows():
    t50, t90 = row['t50'], row['t90']
    f = weibull_cdf(**weibull_params({t50: 0.50, t90: 0.90}))
    x = np.clip(df.index - year, 0, np.inf)
    cdf = list(map(f, x))
    pdf = [0] + [j - i for i, j in zip(cdf[: -1], cdf[1 :])]
    activearea = row['Area']
    activeareacount = []
    for prob in range(len(pdf)):
        activearea = activearea*(1-pdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
        activeareacount.append(activearea)
#                   area_disposed_of_generation_by_year = [element*row['Area']*(1-row['mod_Repairing']) for element in pdf]


    df['mod_Repairing']=0
    activearea = row['Area']
    activeareacount = []
    for prob in range(len(pdf)):
        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
        activeareacount.append(activearea)

    activearea = row['Area']
    activeareacount3 = []
    for prob in range(len(pdf)):
        activearea = activearea*(1-pdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
        activeareacount3.append(activearea)
        
    df['mod_Repairing']=0.2
    activearea = row['Area']
    activeareacount2 = []
    for prob in range(len(pdf)):
        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
        activeareacount2.append(activearea)


    activearea = row['Area']
    activeareacount4 = []
    for prob in range(len(pdf)):
        activearea = activearea*(1-pdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
        activeareacount4.append(activearea)
        
        
        
    plt.plot(activeareacount, label='CDF 0 Repair')
    plt.plot(activeareacount2, label='20% repair')
    plt.plot(activeareacount3, label='PDF 0 repair')
    plt.plot(activeareacount4, label='20% repair')

    plt.legend()
    
    
    
    


# In[ ]:


df['mod_Repairing']=0
df['mod_Repowering']=0                    
activearea = row['Area']
activeareacount2 = []
for prob in range(len(pdf)):
    activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
    if prob == row['mod_lifetime']:
        activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
    activeareacount.append(activearea)

df['mod_Repairing']=0
df['mod_Repowering']=0.5
activearea = row['Area']
activeareacount2 = []
for prob in range(len(pdf)):
    activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
    if prob == row['mod_lifetime']:
        activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
    activeareacount2.append(activearea)

plt.plot(activeareacount, label='CDF 0 Repair')
plt.plot(activeareacount2, label='50% Repower')
plt.legend()


# In[ ]:



                    df['mod_Repairing']=0
                    df['mod_Repowering']=0                    
                    activearea = row['Area']
                    activeareacount = []
                    for prob in range(len(pdf)):
                        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
                        if prob == row['mod_lifetime']:
                            activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                        activeareacount.append(activearea)
                    
                    df['mod_Repairing']=0
                    df['mod_Repowering']=0.5
                    activearea = row['Area']
                    activeareacount2 = []
                    for prob in range(len(pdf)):
                        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
                        if prob == row['mod_lifetime']:
                            print(activearea)
                            activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                            print(activearea)
                        activeareacount2.append(activearea)


                    df['mod_Repairing']=0
                    df['mod_Repowering']=1                    
                    activearea = row['Area']
                    activeareacount3 = []
                    for prob in range(len(pdf)):
                        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
                        if prob == row['mod_lifetime']:
                            activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                        activeareacount3.append(activearea)
                                                
                    plt.semilogy(activeareacount, label='CDF 0 Repower')
                    plt.semilogy(activeareacount2, label='50% Repower')
                    plt.semilogy(activeareacount3, label='100% Repower')
                    plt.legend()
                    
                    plt.figure()
                    plt.plot(activeareacount, label='CDF 0 Repower')
                    plt.plot(activeareacount2, label='50% Repower')
                    plt.plot(activeareacount3, label='100% Repower')
                    plt.legend()
                    
                    df['mod_Repairing']=0
                    df['mod_Repowering']=1                   
                    activearea = row['Area']
                    activeareacount = []
                    for prob in range(len(pdf)):
                        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
                        if prob == row['mod_lifetime']:
                            activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                        activeareacount.append(activearea)
                    
                    df['mod_Repairing']=0.5
                    df['mod_Repowering']=1
                    activearea = row['Area']
                    activeareacount2 = []
                    for prob in range(len(pdf)):
                        activearea = activearea*(1-cdf[prob]*(1-df.iloc[prob]['mod_Repairing']))
                        if prob == row['mod_lifetime']:
                            activearea = 0+activearea*df.iloc[prob]['mod_Repowering']
                        activeareacount2.append(activearea)

                    plt.plot(activeareacount, label='CDF 0 Repair')
                    plt.plot(activeareacount2, label='50% Repair')
                    plt.legend()
                    plt.figure()
                    plt.semilogy(activeareacount, label='CDF 0 Repair')
                    plt.semilogy(activeareacount2, label='50% Repair')
                    plt.legend()


# In[ ]:



import CEMFC
import pandas as pd

file = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_modules_US.csv'
fileglass = r'C:\Users\sayala\Documents\GitHub\CircularEconomy-MassFlowCalculator\CEMFC\baselines\baseline_material_glass.csv'
r1 = CEMFC.Simulation()
r1.createScenario(name='standard', file=file)
r1.scenario['standard'].addMaterial('glass', fileglass )

df = pd.concat([r1.scenario['standard'].data, r1.scenario['standard'].material['glass'].materialdata], axis=1, sort=False)

