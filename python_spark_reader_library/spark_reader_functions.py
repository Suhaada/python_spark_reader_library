#!/usr/bin/env python
# coding: utf-8

# In[1]:

'''  code that exists outside of a class of a function, will run every time somebody imports your library'''

import pyspark
from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark import SparkContext
import pyspark.sql
from pyspark.sql import SQLContext
from pyspark.sql.functions import col
from pyspark.sql.types import *
#import urllib.request
#from io import StringIO
#import spark 


# In[2]:

'''
Function creates a local spark session for this demo 

'''

def create_session(): 
    
    spark = SparkSession     .builder    .appName("read_files")     .getOrCreate()
    
    return(spark)


# In[3]:


'''
Function reads csv or json file defined by 'filename' into a spark dataframe 
   - Arg 1 'filename': filename and location if not in workdir 
   - Arg 2 'header': does it have a header, takes true or false. Defaults to 'true' if argument not provided
   - Arg 3 'multiline': for json files only, true or false. Defaults to false. Indicates if json file is in multiline format
'''

def read_file(filename, header = 'true', multiline = 'false'): 
    
    # initiate sparkcontext if not exist to read into
    spark = SparkSession     .builder    .appName("read_files")     .getOrCreate()
    
    # checks if extension is csv, if yes reads csv into spark dataframe 
    if(filename[-4:] == '.csv'): 
        return(spark.read.load(filename, format = 'csv', sep = ',', header = header))    
    
    # checks if extension is json, reads into spark dataframe 
    elif(filename[-4:] == 'json'): 
        return(spark.read.load(filename, format = 'json', sep = "true", header = header, multiline = multiline))
     
    # in case extension is not csv or json, returns error 
    else: 
        print("##ERROR: file is not in csv or json format #################")
       


# In[4]:


'''
Function takes a dataframe and a list with 2 elements (column name and StringType). 
Casts column types to provided types or returns error. 
    - Arg 1 'dataframe': spark dataframe 
    - Arg 2 'columns': list with 2 elements - 1st item is column name, 2nd item column type. 
    
List of data types: https://spark.apache.org/docs/latest/sql-ref-datatypes.html
Example list: 
            columns_to_cast = [ ('column1', 'StringType()'), 
                               ('column2','StringType()'), 
                               ('column3','IntegerType()'),
                              ('column4','StringType()')]

Note: Casting a string column to Float can result in loss of data. In case column had strings, that'll default to nulls. 
'''

def column_caster(dataframe, columns): 
    
    try: 
        
        for i,j in columns: 
            dataframe = dataframe.withColumn(i,col(i).cast(eval(j)))
    
        return(dataframe)
    
    except: 
        print('Column value couldnt be casted, please check data types!')


# In[5]:


'''
NULL_CHECK function takes 2 arguments: 
    - Arg 1 'dataframe': a spark dataframe 
    - Arg 2 'columns': a list containing the column names to be checked, f.e: columns = ('user','motorcycle','km')
    
Function returns columns with NULL values 
'''

def null_check(dataframe, columns = ''): 
    
    # creates empty list to append column names with null values to 
    null_error = list()
    
    # loops through each columns 
    for i in columns: 

        
        # checks if column contains null values. larger than 1 if yes
        check = dataframe.select("*").where(col(i).isNull())
        check = len(check.head(1))
        
        # if column contains null values, appends them to null_error list 
        if(check >= 1): 
             null_error.append(i)
    
    # returns columns with null values
    return(null_error)
 


# In[6]:


'''
Function takes a dataframe, a list of columns and a regular expression. Looks for regex in provided list of columns, 
and returns which columns contains the regex or warns if none
    - Arg 1 'dataframe': a spark dataframe
    - Arg 2 'columns': a list containing the column names 
    - Arg 3 'regex': expression to look for

Function returns columns where not every field contains regex provided

'''

def regex_check(dataframe, columns, regex): 
    
    # empty list to append to
    regex_list = list()
    
    # loops through each column 
    for i in columns: 

        # checks if column contains regex provided, larger than 1 if yes 
        check = dataframe.filter(dataframe[i].rlike(regex))
        check = check.count()
        
        # if column contains regex, stores it in regex_list
        if(check != dataframe.count()): 
            regex_list.append(i)
            
        elif(check == 0): 
            pass
        
    return(regex_list)


# In[7]:


'''
Unique_check function checks if provided dataframe column contains null values 
    -Arg 1 'dataframe': takes a spark dataframe 
    - Arg 2 'columns': takes a list containing column names to check 
    
Retruns list of columns with non-unique values
'''


def unique_check(dataframe, columns): 
    
    # empty list to append non-unique cols to 
    nonunique_cols = list()
    
    # loops through each column 
    for i in columns: 
        
        # case if column only has unique values 
        if( (dataframe.select(i).distinct().count() == dataframe.count()) == False ): 
            nonunique_cols.append(i)

        # case if column has non-unique values
        elif( (dataframe.select(i).distinct().count() == dataframe.count()) == True ): 
            pass
    
    # returns list of columns with non-unique values
    return(nonunique_cols)


# In[8]:


'''
FUNCTION TAKES 4 ARGUMENTS: 
    - Arg 1 'filename': path and name of csv or json file to be checked
    - Arg 2: 'header': indicates if file to read has header 
    - Arg 3 'multiline': only for json files, defaults to false. Indicates if json is multiline
    - Arg 2 'columns_to_cast': column names for which type needs to be casted. If not provided, function doesn't case types
    - Arg 3 'columns':  list of columns to perform the checks on. If not provided, all columns will be checked 
    - Arg 4 'regex': provide value if you need to make sure column contain a given expression 
    
Function: 
    1) reads cvs / json file provided
    2) casts column types if provided
    3) checks if column(s) contain null values
    4) checks if column(s) contain specified expression in all fields
    5) checks if column(s) has non-unique values 
    6) if any of the below is true, returns error 
    7) otherwise returns dataframe 

'''


def check_my_data(filename, columns_to_cast = '', columns = '', regex = '', header = 'true', multiline = 'false'): 
    
    # get dataframe 
    df = read_file(filename, header = header, multiline = multiline)
    
    # cast columns if provided
    if(len(columns_to_cast)>0):
        df = column_caster(df, columns_to_cast)
    else: 
        pass
    
    # get columns if not provided
    if(len(columns)==0):
        columns=df.columns
    else: 
        pass
    
    # returns cols with NULL values 
    nc = null_check(df, columns)
    
    # returns cols where not all field contains REGEX 
    reg_check = regex_check(df, columns, 'bsn')
    
    # returns list of columns with non-unique values
    u_check = unique_check(df, columns)
    
    # logical checks
    if(len(nc + reg_check + u_check)>0): 
        print('DATA QUALITY ERROR, VALIDATION FAILED AT: ')
    
    if(len(nc)>0): 
        print('FIELD HAS NULLS: '), print(nc)

    if(len(reg_check)>0): 
        print('REGEX IS NOT IN ALL FIELDS IN: '), print(reg_check)

    if(len(u_check)>0): 
        print('NON-UNIQUE FIELDS IN: '), print(u_check)

    if(len(nc + reg_check + u_check)==0): 
        print('DATA SUCCESSFULLY LOADED!'), print(df.show(5))
        
        # if data is ready, return dataframe 
        return(df)
        

