# Nagios example for an ETL to a mysql database

---

## Code Purpose

This is a very simple code to extract data from a nagios url and upload it to a
mySQL/MariaDB database. It's original purpose was to get the data to be
displayed on a grafana container and a graph monthly uptimes.

Every step is on a separate module and every module code can be reused alone.

1. Get the csv files via curl and store them in a folder
2. Add date columns to the csv file (in this case year and month) and
   consolidate all downloaded files in one file.
3. Finally upload the data to the databse
4. as an Option, send the gererated csv file attached by mail (backup)

Code is full commented. Parameters are on main module excepts for the databse
connection.

Asumtions:

-   database and table already exist on destiny

### Install notes:

-   For linux, you will need to install python (most of times already
    installed), mysql client, libcurl4-gnutls-dev and librtmp-dev.

```
sudo apt install libcurl4-gnutls-dev librtmp-dev
sudo apt install mysql-client-8.0
pip install -r requirements.txt
```
