#!/usr/bin/env python
# coding: utf-8

# In[13]:


import datetime
import tables
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker

import sapphire
from sapphire import esd
from sapphire.time_util import GPSTime


# In[14]:


# This function will take start and end times as input and return the corresponding event rate and time variables
def xyvalues(filename, start, end):

    # Creating array that holds timestamp of events occurred during times of interest
    timestamp = np.loadtxt(filename, usecols = (2),unpack=True)

    # Calculating and creating time and event rate variables for plot
    alltime = [] # This holds all of the event timestamps
    time = [] # This holds average event rate timestamps only
    event_rate = []
    event_ratefit = []
    event_count = 0
    rate_time = 1000
    rate_interval = start + rate_time # 300 is used to calculate event rate (in Hz) for every 5 mins (300 seconds)

    for x in timestamp:
        if start < x < end: 
            if x < rate_interval and (end - x) > 10:
                event_count += 1
            else:    
                time.append(GPSTime(x).description())
                alltime.append(x)
                
                if event_count == 0:
                    event_rate.append(np.nan)
                    event_ratefit.append(0)
                else: 
                    event_rate.append(event_count / rate_time)
                    event_ratefit.append(event_count / rate_time)
                event_count = 0
                rate_interval += rate_time
    
    return time, event_rate, alltime, event_ratefit


# In[17]:


# Start and end times for dates of interest
start1 = GPSTime(2016, 12, 1).gpstimestamp()
end1 = GPSTime(2017,1,1).gpstimestamp()

start2 = GPSTime(2016, 9, 1).gpstimestamp()
end2 = GPSTime(2016, 10,1).gpstimestamp()

start3 = GPSTime(2016, 6, 1).gpstimestamp()
end3 = GPSTime(2016, 7,1).gpstimestamp()

start4 = GPSTime(2016, 3, 1).gpstimestamp()
end4 = GPSTime(2016, 4,1).gpstimestamp()

# Files being used
winter16 = "dec16.tsv"
fall16 = "sept16.tsv"
summer16 = "june16.tsv"
spring16 = "march16.tsv"

#Using xyvalues function to create time and event rate variables for each one of the seasons
t1,e_rate1, at1, erfit1 = xyvalues(winter16, start1, end1)
t2,e_rate2, at2, erfit2 = xyvalues(fall16, start2, end2)
t3,e_rate3, at3, erfit3 = xyvalues(summer16, start3, end3)
t4,e_rate4, at4, erfit4 = xyvalues(spring16, start4, end4)

# Plotting event rate vs time for each season
p1 = plt.plot(t4,e_rate4, label = 'spring')
plt.setp(p1, linewidth=2, color='yellowgreen')
p2 = plt.plot(t3,e_rate3, label = 'summer')
plt.setp(p2, linewidth=2, color='gold')
p3 = plt.plot(t2,e_rate2, label = 'fall')
plt.setp(p3, linewidth=2, color='darkorange')
p4 = plt.plot(t1,e_rate1, label = 'winter')
plt.setp(p4, linewidth=2, color='dodgerblue')

#These variables serve to plot each one of the trendlines independently
time = t1 + t2 + t3 + t4

timesummer   = t3
atsummer     = at3
e_ratesummer = erfit3

timefall   = t2
atfall     = at2
e_ratefall = erfit2

timewinter   = t1
atwinter     = at1
e_ratewinter = erfit1

timespring   = t4
atspring     = at4
e_ratespring = erfit4

#Creating and plotting trendlines
fitsummer = np.polyfit(atsummer, e_ratesummer, 1)
flinesummer = np.poly1d(fitsummer)
plt.plot(timesummer, flinesummer(atsummer),color="red", linewidth=2, label ='trendline', linestyle="--")

fitfall = np.polyfit(atfall, e_ratefall, 1)
flinefall = np.poly1d(fitfall)
plt.plot(timefall, flinefall(atfall),color="red", linewidth=2, linestyle="--")

fitwinter = np.polyfit(atwinter, e_ratewinter, 1)
flinewinter = np.poly1d(fitwinter)
plt.plot(timewinter, flinewinter(atwinter),color="red", linewidth=2, linestyle="--")

fitspring = np.polyfit(atspring, e_ratespring, 1)
flinespring = np.poly1d(fitspring)
plt.plot(timespring, flinespring(atspring),color="red", linewidth=2, linestyle="--")

#Setting the plot format
plt.xticks(np.arange(0, len(time) + 1, 400)) # Used to set number of x values shown in axis (make it readable)
plt.xticks(rotation=70)
#plt.ylim(0.0,0.8)
plt.legend()
plt.grid()
plt.rcParams['figure.figsize']=[20,6]
plt.xlabel("Time [GPS]",fontsize=12)
plt.ylabel("Event Rate [Hz]",fontsize=12)
plt.title("Seasonal Event Rate in 2016",fontsize=12)


plt.show()


# In[ ]:





# In[ ]:




