# -*- coding: utf-8 -*-
"""

@author: akhushalani

You can find the data here - https://en.wikipedia.org/wiki/List_of_Monster_Energy_NASCAR_Cup_Series_champions

"""

import pandas as pd
import numpy as np
import seaborn as sns
import pyodbc

#Read csv file using path of the file
#When using path add r - this will make the string raw
df = pd.read_csv(r'C:\Users\Username\Documents\FolderName\NASCAR Champion History Dataset.csv')

#Or Change the slash
#df1 = pd.read_csv("C:/Users/Username/Documents/FolderName/NASCAR Champion History Dataset.csv")

#Convert a JSON File to Pandas-------------------------------------------------
data = pd.read_json("data.json", lines= True)
data.head(10)
df_gd = pd.DataFrame(data)
#Format the data as a list of dict objects
data_dict = [{'data': x} for x in df_gd['data']]
# Create a DataFrame with json_normalize
data_df = pd.io.json.json_normalize(data_dict)
# Convert objects to a numeric datatype if possible
data_df = data_df.convert_objects(conver_numeric=True)

#Connect to DB-----------------------------------------------------------------

server = 'server'
database = 'name'
username = 'username'
password = 'password'
driver = 'Drivername'


def connect_sql_server(server, database, username, password, driver):
        conn_string = 'DRIVER={' + driver + '};' + 'SERVER=' + server + ';' + 'DATABASE=' + database + ';' \
                      + 'Uid=' + username + ';' + 'pwd=' + password + ';'
        conn = pyodbc.connect(conn_string, autocommit=True)
        return conn

# Manage connections for pandas and pyodbc
cnxn = connect_sql_server(server, database, username, password, driver)

#Sql 
sql1 = 'Select * from tablename'
data = pd.read_sql(sql1, cnxn)

#Rename the columns------------------------------------------------------------
df.rename(columns={'Driver':'Name','Car Number': 'no'},inplace=True)

#Insert column with a specific range of numbers as ID -------------------------
df.insert(0, 'New_ID', range(91, 91 + len(df)))

#Inserting few more columns for demo purposes
df.insert(6, 'max_spd', range(100, 100 + len(df)))
df.insert(7, 'max_rpm', range(1000, 1000 + len(df)))

#Name the columns in the dataframe---------------------------------------------
df.columns

#Shape of the data-------------------------------------------------------------
df.shape

#Data types of the columns-----------------------------------------------------
df.dtypes

#Make a copy of dataframe -----------------------------------------------------
new = df.copy()

#Select some columns to work with(subsetting)----------------------------------
df1 = df[["New_ID","max_spd","max_rpm","no"]]

#Extract Unique value----------------------------------------------------------
df["no"].unique()

#Drop a column-----------------------------------------------------------------
df = df.drop(columns=["max_spd"])
df.drop(columns=["max_rpm"], inplace = True)

#Filter column by row value----------------------------------------------------
#Filtering has many options 

#Approach 1 with one condition
filter_1 = new[(new["max_spd"] > 105)]
filter_2 = new.query('no == 3.')

#Approach 2 with two conditions
filter_3 = new[(new["max_spd"] > 106) & (new["max_rpm"] > 1005 )]
filter_4 = new.query('Wins > 2 & no == 14')

#Accessing a particular row value
x = new[new["no"] == 36]

#Randomly select some fraction of the data ------------------------------------
df_percent = new.sample(frac=0.02)

#Calculate average max_spd grouped by car -------------------------------------
df_percent["max_spd"] = df_percent.groupby("no").max_spd.mean()

#Group by function-------------------------------------------------------------
df_g = df.groupby("no")

#Accessing groups -------------------------------------------------------------
df_g.first()
df_g.get_group(88) 

#Convert dataframe column to int-----------------------------------------------
df = df.astype({"Year": int})

#Mulitivariate Analysis--------------------------------------------------------
sns.set()
cols = ["no","max_spd","max_rpm"]
sns.pairplot(new[cols], size = 3.0)

#Create a new pandas dataframe with columns - new-1, new-2---------------------
empty = pd.DataFrame(columns=["new-1","new-2"])

#Concat two dataframes---------------------------------------------------------
#This basically appends two dataframes so if there are 6 columns in each 
#filter_1 & filter_2, concat will give a new dataframe with 12 columns
sample = pd.concat([filter_1,filter_2], axis=1, sort = False)

#Merge two dataframes----------------------------------------------------------
merged = filter_1.merge(filter_2, on= ["no"])

#Use standard scaler-----------------------------------------------------------
from sklearn.preprocessing import StandardScaler
ss = StandardScaler()
new[['max_spd','max_rpm']] = ss.fit_transform(new[['max_spd','max_rpm']])

#Outliers Detection------------------------------------------------------------

#Modified Z Score
def modified_z_score(ys):
    median_y = np.median(ys)
    median_absolute_deviation_y = np.median([np.abs(y - median_y) for y in ys])
    modified_z_scores = [0.6745 * (y - median_y) / median_absolute_deviation_y
                         for y in ys]
    return np.abs(modified_z_scores) #Then based on threshold next step is determined






