## mysqlupload.py
## upload a given file to a table in database. Both needs to exists before upload
import csv
import mysql.connector as mysql

def conection():
  db = mysql.connect(
     host="mysqhostaddress",
     user="mysqluser",
     password="mysqlpassword",
     database="uptime", # you name it
     auth_plugin='mysql_native_password',
     )
  
  return db

def queryrows(tablename,year): 
  db = conection()
  cursor = db.cursor()
  cursor.execute("select count(*) from " + tablename + " where year="+str(year))
  rows =cursor.fetchone()
  return rows[0]

def erasedata(tablename, year): 
  db = conection()
  cursor = db.cursor()
  cursor.execute("delete from "+ tablename + " where year="+str(year))
  db.commit()
  cursor.close()
  print("Year data deleted on " + tablename + " : " + str(queryrows(tablename,year)) + " (rows)")

def loaddata(outputdir, filename, tablename, year):   #Load data from CSV
  erasedata(tablename, year)
  db = conection()
  cursor = db.cursor()
  csvfile = csv.reader(open(outputdir + "/" + filename,'r'),quoting=csv.QUOTE_NONNUMERIC)
  sqlleft =""
  sqlright =""
  for index,row in enumerate(csvfile):
    if index==0: # sqlleft is generated only with the first row
        row = ",".join(row)
        sqlleft = "insert into "+ tablename + "(" +row+ ") VALUES ("

    else:  # sqlright is generated for every next row and inserted into db
        row = [x.strip('%') for x in row] # strip % on files
        row[0]="\""+ row[0] +"\"" # Convert to string first hostname field
        row = ",".join(row)
        sqlright = row+")"
        cursor.execute(sqlleft+sqlright)
  db.commit()
  cursor.close()

  print("data loaded on table " + tablename + " : " + str(queryrows(tablename,year)) + " (rows)")

if __name__ == "__main__":

  # parameters
  outputdir = 'output'
  targetfile = "nagiosdata.csv" # output file
  tablename = "uptime.nagiosdata"  ## database.tablename
  year = 2023    #year

  #routine
  loaddata(outputdir, targetfile, tablename, year)  # loads data into database.table


