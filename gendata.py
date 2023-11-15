## gendata.py
## Takes al files.csv on location and generate one targetfile on outputdir with two extra columns (year and month)

import os
import csv

def gendata(targetfile,location,outputdir):

    if  not  os.path.exists(outputdir):
        os.mkdir(outputdir)
    
    fulloutput = outputdir + "/" + targetfile

    try:  # deletes target file if exists
        os.remove(fulloutput)
    except OSError as err:
        pass # no an error if file is not found

    allfiles = os.listdir(location) # get all files in source location
    allfiles.sort() 

    # Will join all files in location adding a year and month columns
    for numfile,filename in enumerate(allfiles):
        fileyear=filename[2:6]   # get year from filename as it was generated that way
        filemonth=filename[7:9]  # get month from filename as it weas generated that way

        fullname = os.path.join(location,filename)

        with open(fullname,'r') as filein:
            with open(fulloutput,'a') as fileout:
                writer = csv.writer(fileout,quoting=csv.QUOTE_NONNUMERIC)
                reader = csv.reader(filein)
                for index, row in enumerate(reader):
                    if index == 0 and numfile == 0 : # first file, first row is title row
                        row = [x.strip(' ') for x in row] # strip whitespaces from title row
                        row.append('YEAR')  # add year column
                        row.append('MONTH') # add month column
                        writer.writerow(row) 
                    elif index == 0 :
                        continue # ignores first row in next files
                    else:
                        row.append(fileyear)   # add year
                        row.append(filemonth)  # add month
                        writer.writerow(row)
                print(fullname," ",(reader.line_num -1), " rows") # number of row (not counting title)
            fileout.close()
        filein.close()
    

    print(targetfile, " generated")


if __name__ == "__main__":
    targetfile = 'nagiosdata.csv'
    location = 'files'
    outputdir = 'output'
    gendata(targetfile,location,outputdir)