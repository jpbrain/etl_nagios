## getfiles.py
## Routine to export files as csv from a nagios server/application for a given year

import os
import pycurl
import certifi
from datetime import datetime

def isleap(year):
	return not year % 4 and (year % 100 or not year % 400)

# builds url to query from nagios 
def geturl(server,iday,imonth,iyear,eday,emonth,eyear): 
    urlbase = server \
              + "nagios/cgi-bin/avail.cgi?show_log_entries=&service=all&timeperiod=custom&smon=" \
              + str(imonth) + "&sday=" + str(iday) +"&syear=" + str(iyear) \
              + "&shour=0&smin=0&ssec=0&emon=" \
              +  str(emonth) +"&eday="+ str(eday) + "&eyear="+ str(eyear) \
              + "&ehour=24&emin=0&esec=0&rpttimeperiod=&assumeinitialstates=yes&assumestateretention=yes&assumestatesduringnotrunning=yes&includesoftstates=no&initialassumedservicestate=6&backtrack=4&csvoutput="

    return urlbase


def deletefiles(location):

    # source location hast to be empty to avoid duplicate data
    for f in os.listdir(location):
        try:  
            os.remove(os.path.join(location,f))
        except OSError as err:
            print ("Error deleting file : ", err)

#download one file from nagios server
def getfile(server,filename,iday,imonth,iyear,eday,emonth,eyear): 
    curlString = geturl(server,iday,imonth,iyear,eday,emonth,eyear)
    with open(filename,"wb") as filename:
        curl = pycurl.Curl()
        curl.setopt(curl.URL,curlString)
        curl.setopt(curl.WRITEDATA, filename)
        curl.setopt(curl.CAINFO, certifi.where())
        curl.perform()
        curl.close()


# get every finished month file in a year from Server on location to download files
def downloadfiles(server, location, year): 
    thismonth = datetime.now().month
    thisyear = datetime.now().year
    monthdays = [31,28,31,30,31,30,30,31,30,31,30,31]

    deletefiles(location)

    if isleap(year):
        monthdays[1]=29 # modifies February
        print("-->> Is a leap year")
    
    for i in range(1,13):
        filename = "S-"+str(year)+"-"+"{:02.0F}".format(i)+".csv"

        # if it is current year will only get the file for finiched months
        # if thismonth is January will get all 12 months
        if i< thismonth or year < thisyear or (thismonth == 1 and year < thisyear):  
            getfile(server,"./"+location+"/"+filename,1,i,year,monthdays[i-1],i,year)
            
    
if __name__ == "__main__":

    # General parameters
    year = 2023    # year
    location = 'files' # download directory
    server = "http://nagiosadmin:nagios@nagios.yourserver.com/" #your nagios hosta and access information

    print("processing year : ",year)
    downloadfiles(server,location,year)    # download files
