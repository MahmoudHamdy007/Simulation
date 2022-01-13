import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
df=pd.read_csv('newSheet.csv')
service_df=pd.read_csv('serv.csv')
def calc_Cumulative(probabilty):
    df['Cumulative']=np.cumsum(probabilty)
probabilty=df['Probability'] 
calc_Cumulative(probabilty)
df['From']=[0,0,0,0,0,0,0,0]
df['To']=[0,0,0,0,0,0,0,0]
def tofunc(x):
    return x*1000-1
df['To']=df['Cumulative'].apply(tofunc)
def fromfunc(y): 
    x=df.loc[0,'To']
    return y-x
df['From']=df['To'].apply(fromfunc)
sim_df=pd.DataFrame(columns=['R.V','Time Interval'],
                    data=[[0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0]])
randTime=[]
randService=[]
for i in range(0,8):#Generate a random Values 
    n = random.randint(0,999)
    v =random.randint(0,99)
    randTime.append(n)
    randService.append(v)
sim_df['R.V']=randTime
sim_df['R.V For Services']=randService
for ind,row in sim_df.iterrows():#LookUp()
     if row['R.V'] in range(0,125):
         row['Time Interval']=df.loc[0,'Time Between Arrival']
     if row['R.V'] in range(125,250):
         row['Time Interval']=df.loc[1,'Time Between Arrival']
     if row['R.V'] in range(250,374):
         row['Time Interval']=df.loc[2,'Time Between Arrival']
     if row['R.V'] in range(374,500):
         row['Time Interval']=df.loc[3,'Time Between Arrival']
     if row['R.V'] in range(500,625):
         row['Time Interval']=df.loc[4,'Time Between Arrival']
     if row['R.V'] in range(625,750):
         row['Time Interval']=df.loc[5,'Time Between Arrival']
     if row['R.V'] in range(750,875):
         row['Time Interval']=df.loc[6,'Time Between Arrival']
     if row['R.V'] in range(875,1000):
         row['Time Interval']=df.loc[7,'Time Between Arrival']
sim_df.loc[0,'Time Interval']=0
sim_df.loc[0:,'C.T.A']=0
sim_df.loc[0,'R.V']=0
for ind,row in sim_df.iterrows():#Calculating the clock time for arrival
    sim_df.loc[ind:,'C.T.A']=row['Time Interval']+row['C.T.A']
sim_df['Start']=0
sim_df['End']=0
sim_df['Serv. Duration']=0
for ind,row in sim_df.iterrows():#LookUpForServices Duration()
     if row['R.V For Services'] in range(0,30):
         row['Serv. Duration']=service_df.loc[0,'Service time']
     if row['R.V For Services'] in range(30,58):
         row['Serv. Duration']=service_df.loc[1,'Service time']
     if row['R.V For Services'] in range(58,83):
         row['Serv. Duration']=service_df.loc[2,'Service time']
     if row['R.V For Services'] in range(83,100):
         row['Serv. Duration']=service_df.loc[3,'Service time']
         #sim_df.loc[ind:,'Start']=(row)['C.T.A']  

sim_df.loc[0,'End']= sim_df.loc[0,'Start']+sim_df.loc[0,'Serv. Duration']#First Row
sim_df.loc[0,'System State']=0
for ind in range(1,8):
    sim_df.loc[ind,'Start']= max(sim_df.loc[ind-1,'End'],sim_df.loc[ind,'C.T.A'])
    sim_df.loc[ind,'End']=sim_df.loc[ind,'Start']+sim_df.loc[ind,'Serv. Duration']
    if sim_df.loc[ind,'Start'] > sim_df.loc[ind-1,'End']:
        sim_df.loc[ind,'System State'] = sim_df.loc[ind,'Start'] - sim_df.loc[ind-1,'End']
    else:
        sim_df.loc[ind,'System State']=0
plot_df=pd.DataFrame(columns=['Customer No.','Clock Time'],
                    data=[
                         [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0],
                          [0,0]])
i=0
j=0
while i < 16:
      plot_df.loc[i,'Customer No.']= j
      i+=1
      plot_df.loc[i,'Customer No.']= j
      if i %2 ==0 :
          j+=1
i=0
k=0
while i <16:
    plot_df.loc[i,'Clock Time']=sim_df.loc[k,'C.T.A']
    i+=1
    plot_df.loc[i,'Clock Time']=sim_df.loc[k,'End']
    k+=1
    i+=1
plot_df.dropna(subset = ["Clock Time"], inplace=True)
plot_df.sort_values(by=['Clock Time'])
print("__________________________Arrival Probability_______________________________\n") 
print(df)
print("__________________________Service Probability________________________________\n")
print(service_df)
print("__________________________Simulation Table__________________________________\n")
print(sim_df)
print("______________________________________________________________________________\n")
print(plot_df)
x=plot_df['Clock Time']
y=plot_df['Customer No.']
plt.scatter(x, y)
plt.plot(x, y)
plt.title("Chronological Ordering of Events")
plt.xlabel("Clock Time")
plt.ylabel("Customer No.")
plt.show()
df.to_csv('Customer.csv',index=False)
sim_df.to_csv('Simulation Table.csv',index=False)
