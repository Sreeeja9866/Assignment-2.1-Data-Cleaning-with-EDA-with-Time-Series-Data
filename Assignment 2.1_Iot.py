#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning with EDA and Time Series Data

# In[1]:


#importing additional libraries and helper functions
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# # Loading and Cleaning Data

# In[28]:


#The data set has mixed data types which casusing a warning
df_raw = pd.read_csv("household_power_consumption.txt", delimiter = ";")
# drop any rows with missing values
df_clean = df.dropna()


# In[29]:


#Printing the rows
df_raw.head()


# In[30]:


#Summary of descriptive statistics for the numerical columns below
df_raw.describe()


# In[31]:


#Displays the data type of each column
df_raw.dtypes


# In[32]:


#creating a copy of main data
df = df_raw.copy()


# In[33]:


#Creating new DateTime column
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')


# In[34]:


#Displays the datatype of each column 
df.dtypes


# In[35]:


#converting all columns in the df DataFrame to numeric values and non-numeric values are converted to NaN values
df = df.apply(pd.to_numeric, errors='coerce')


# In[36]:


#Displays the datatype of each column 
df.dtypes


# In[38]:


#Converting the 'Datetime' column in the df DataFrame to a datetime format, and then creating new 'Date' and 'Time' columns containing the corresponding date and time components of the 'Datetime' column.
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Date'] = df['Datetime'].dt.date
df['Time'] = df['Datetime'].dt.time


# In[39]:


#Displays the datatype of each column
df.dtypes


# In[40]:


#Displays the value in the first row of the 'Date' column 
df.Date[0]


# In[41]:


#Displays the value in the first row of the 'Time' column 
df.Time[0]


# In[42]:


#use datetime_is_numeric = True to get statistics on the datetime column
desc = df.describe(datetime_is_numeric = True)

#force the printout not to use scientific notation
desc[desc.columns[:-1]] = desc[desc.columns[:-1]].apply(lambda x: x.apply("{0:.4f}".format))
desc


# In[43]:


#creating a bar plot that shows the number of missing values in each column 
df.isna().sum().plot.bar()


# In[44]:


#calculating the total number of NaN values in each column of the df for each date, and then creating a line plot of the NaN values over time for all columns except 'Date', 'Datetime', and 'Time
df_na = df.drop('Date', axis = 1).isna().groupby(df.Date, sort = False).sum().reset_index()
df_na.plot('Date', df_na.columns[3:-1])


# Q)What do you notice about the pattern of missing data?
# 
# A.The graph indicates that the amount of missing data is roughly consistent across all variables.
# 
# Q)What method makes the most sense to you for dealing with our missing data and why? (There
# isn't necessarily a single right answer here)
# 
# A. Deletion: This involves getting rid of any observations that have missing data. This approach is
# straightforward and easy to use, if the data are not fully absent at random, it might result in
# inaccurate estimations. In certain circumstances, eliminating data might also result in a reduction
# in statistical output.
# 
# Imputation: This involves replacing the missing values with estimates based on the other data
# available. Imputation can be a good choice if the data is missing at random.
# 
# Model-based imputation: This involves using a model to estimate the missing values. This
# approach can be especially useful when the data is missing not at random because it can take
# into account the relationship between the missing data and other variables in the dataset.
# 
# 
# 

# In[45]:


#Dropping all the missing values
df = df.dropna()
df.isna().sum().plot.bar()


# In[46]:


#use datetime_is_numeric = True to get statistics on the datetime column
desc = df.describe(datetime_is_numeric = True)
#force the printout not to use scientific notation
desc[desc.columns[:-1]] = desc[desc.columns[:-1]].apply(lambda x: x.apply("{0:.4f}".format))
desc


# # Visualizing the data

# Q)Which variables did you choose and why do you think they might be interesting to compare to each other over time? Remember that data descriptions are available at the data source link at the top of the assignment.
# 
# A.I have selected Global_active_power, Global_reactive_power, Voltage, and Global_intensity variables from the dataset to plot over time. Global_active_power and Global_reactive_power represent the overall active and reactive power usage in the household, respectively. Meanwhile, Global_intensity denotes the total current consumption of the household, and Voltage tracks the voltage levels in the residence.
# 

# In[47]:


# Converting the date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])
# Selecting the variables
variables = ['Global_active_power','Global_reactive_power','Global_intensity','Voltage']
# Creating line charts
fig, axs = plt.subplots(len(variables), 1, figsize=(10, 12), sharex=True)
for i, variable in enumerate(variables):
    axs[i].plot(df['Date'], df[variable])
    axs[i].set_ylabel(variable)
    axs[i].set_title('Line Chart of ' + variable + ' over Time')
# Add x-axis label to bottom subplot
axs[-1].set_xlabel('Time')
# Show chart
# adjust subplot spacing
plt.subplots_adjust(hspace=0.5)


# Q)What do you notice about visualizing the raw data? Is this a useful visualization? Why or why not?
# 
# A.Visualizing raw data can provide insight into general trends and patterns that have developed over time, but it may be difficult to draw meaningful conclusions without additional processing or analysis.
# In the case of the four selected variables, raw data visualization reveals oscillations and patterns, but identifying specific correlations between them can be challenging.
# 
# Therefore, while visualizing raw data can be a helpful initial step in data exploration, it is typically insufficient for drawing accurate conclusions or making precise predictions. To extract meaningful insights, additional preprocessing or analysis may be necessary.
# 

# In[49]:


df_monthly = df_clean.groupby(pd.Grouper(key='Datetime', freq='M')).mean()

# create a figure with four subplots
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 12), sharex=True)

# iterate over the variables and plot them on separate subplots
for i, var in enumerate(variables): 
    ax = axes[i]
    ax.plot(df_monthly.index, df_monthly[var])
    ax.set_ylabel(var)
    
# set x-label for the last subplot
axes[-1].set_xlabel('Time')

# add a title for the entire plot
fig.suptitle('Monthly Average Electricity Consumption')

# adjust subplot spacing
plt.subplots_adjust(hspace=0.5)


# Q)What patterns do you see in the monthly data? Do any of the variables seem to move together?
# 
# A.The monthly data shows that Global_intensity and Global_active_power variables have similar trends over time, while Voltage experienced a sharp decline during the first half of 2007, followed by a consistent increase with a distinct pattern. Global_reactive_power, on the other hand, had two significant drops and rises.
# 
# From these observations, it appears that some variables are correlated with one another. Specifically, Global_intensity and Global_active_power seem to exhibit a similar movement pattern, indicating a potential relationship between the two.
# 

# In[50]:


df.columns


# In[51]:


# Convert Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Specify variables to plot
variables = ['Global_active_power', 'Global_reactive_power', 'Global_intensity', 'Voltage']

# Create subplots for each variable and plot 30-day moving average
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(12, 12))
for i, var in enumerate(variables):
    # Check if variable is present in DataFrame
    if var in df.columns:
        # Compute 30-day moving average for variable
        rolling_avg = df.set_index('Date')[var].rolling('30D').mean()
        ax = axes[i]
        # Plot 30-day moving average
        ax.plot(rolling_avg.index, rolling_avg, color='red')
        ax.set_xlabel('Date')
        ax.set_ylabel(var)
        ax.set_title(f'{var} 30-day Moving Average')
        ax.grid(True)
plt.tight_layout()

# Display plot
plt.show()


# Q)How does the moving average compare to the monthly average? Which is a more effective way to visualize this data and why?
# 
# A.The plot of the 30-day moving average appears to be smoother than the plot of the monthly average,
# as observed by comparing the two charts.
# The reason behind this is that the monthly average plot is calculated using data from only one month, 
# whereas the 30-day moving average considers the previous 30 days of data. Since the 30-day moving average filters out noise
# and presents a clearer picture of the underlying trend, it is generally considered to be a more effective approach for visualizing patterns in the data.
# 

# In[52]:


# Creating a scatter matrix plot of the variables
axes = pd.plotting.scatter_matrix(df[['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity']], diagonal='kde')
corr = df[['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity']].corr().values

for i, j in zip(*plt.np.triu_indices_from(axes, k=1)):
    axes[i, j].annotate("%.3f" %corr[i,j], (0.8, 0.8), xycoords='axes fraction', ha='center', va='center')

plt.show()


# In[ ]:




