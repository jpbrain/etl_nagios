## nagosdata.py
## This main file orchestrates all other modules getfiles, gendata or genpanda, loaddata and send mail
##

# choose one module option you want to use gendata or genpanda
from gendata import gendata
#from genpanda import gendata

from getfiles import downloadfiles
from mysqlupload import loaddata
from sendfile import sendFiles
import os

if __name__ == "__main__":

    # General parameters
    sinceyear = 2023 #intitial year 
    toyear = 2023    #final year
    location = 'files' # download directory
    outputdir = 'output'
    targetfile = "nagiosdata.csv" # output file
    server = "http://nagiosadmin:nagios@nagios.yourserver.com/" #your nagios hosta and access information
    tablename = "uptime.nagiosdata"  ## database.tablename

    MAILSERVER  =  "yoursmtp.domain.org"
    PORT        =  25
    USE_TLS     = False # Make it true to enable authetication
    USERNAME    = "put your username" # Also TLS needs to be True to authenticate
    PASSWORD    = "put your password" # Also TLS needs to be True to authenticate
    FROM        = 'noreply@domain.org'
    TO          = ["email1@domain.org" , "email2@domain.org"] # must be a list
    SUBJECT     = "Content of the email. Ex. Nagios data"
    BODY        = "Automtic file sent. Please do not reply"
    

    #routine
    for year in range(sinceyear,toyear+1):

        print("processing year : ",year)
        downloadfiles(server,location,year)    # download files
        gendata(targetfile,location,outputdir)           # generates new file with year and month columns
        loaddata(outputdir, targetfile, tablename, year)  # loads data into database.table
        
        FILEATTACH  = [os.path.join(outputdir, file) for file in os.listdir(outputdir)]
        sendFiles(MAILSERVER,FROM,TO,SUBJECT,BODY,FILEATTACH,PORT,USERNAME, PASSWORD, USE_TLS )



        
