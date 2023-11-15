## genpanda.py
## Takes al files.csv on location and generate one targetfile on outputdir with two extra columns (year and month)
## Same as gendata but using pandas

import os
import csv
import pandas as pd


def gendata(targetfile,location,outputdir):

    if  not  os.path.exists(outputdir):
        os.mkdir(outputdir)

    allfiles = os.listdir(location) # get all files in source location
    allfiles.sort() 

    outputFrame = pd.DataFrame() # emtyDataframe

    # Will join all files in location adding a year and month columns
    for numfile,filename in enumerate(allfiles):
        fileyear=filename[2:6]   # get year from filename as it was generated that way
        filemonth=filename[7:9]  # get month from filename as it weas generated that way

        fullname = os.path.join(location,filename)

        # Load the CSV data into a DataFrame
        df = pd.read_csv(fullname)
        # Create a new column 
        df['YEAR'] = str(fileyear)
        df['MONTH'] = str(filemonth)

        # Append the DataFrame to ouput
        outputFrame = pd.concat([outputFrame,df])

    outputFrame.columns = outputFrame.columns.str.strip() #strip spaces from header
    outputFrame.to_csv(outputdir +'/'+ targetfile, index=False, quoting=csv.QUOTE_ALL,doublequote=True) # write the output file

if __name__ == "__main__":
    targetfile = 'panda_output.csv'
    location = 'files'
    outputdir = 'output'
    gendata(targetfile,location,outputdir)