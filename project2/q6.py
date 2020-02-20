# This program takes as input a database file and a tsv file containing way elements.
# And inserted each way element into database file accordingly

import csv
import sqlite3
import sys

# main function here
def main():
    # read the input database file and tsv file
    database = sys.argv[1]
    file_name = sys.argv[2]
    
    # open the database file
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    
    c.execute("PRAGMA foreign_keys = on")
    
    # list of values to be inserted into database file later
    waytag = []
    waypoint = []
    way = []
    
    # open the tsv file and read each line
    with open(file_name) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        count = 0
        wayid = 0
        for row in rd:
            closed = 0
            ordinal = 0
            
            waytag_tuple = ()
            way_tuple = ()
            
            # read the first line(contains wayid and waytag values) 
            # in two consecutive non-blank lines of the way element
            if count%2 == 0:
                wayid = row[0]
                count = count + 1
                try:
                    int(row[0])
                except ValueError:
                    print("Please make sure the input tsv file's first colmn of first line is wayid.")
                    return
                
                for index in range(1, len(row)):
                    waytag_tuple = waytag_tuple + (wayid,)
                    
                    try:
                        k, v = row[index].split('=')
                    except ValueError:
                        print("Please make sure waytag is in format 'k = v'.")
                        return
                    
                    waytag_tuple = waytag_tuple + (k,) + (v,)
                    waytag.append(waytag_tuple)
                    waytag_tuple = ()
                  
                  
            # read the second line(contains node id in the waypoint) 
            #in two consecutive non-blank lines of the way element 
            else: 
                count = count + 1
                
                for i in range(0, len(row)):
                    waypoint_tuple = ()
                    waypoint_tuple = waypoint_tuple + (wayid,)
                    waypoint_tuple = waypoint_tuple + (str(i),) + (row[i],)
                    waypoint.append(waypoint_tuple)
                    
                    try:
                        int(row[i])
                    except ValueError:
                        print("Please make sure the input tsv file's second line only contains nodeid.")
                        return                    
                    
                if row[0] == row[len(row) - 1]:
                    closed = "1"
    
                way_tuple = way_tuple + (wayid,) + (closed,)
                way.append(way_tuple)
    
    # insert each values tupe into way table
    for inser in way:
        try:
            c.execute('insert into way (id, closed) values (?, ?)', inser)
        except sqlite3.IntegrityError:
            print("Way: " + inser[0] + " already exist.")
            pass  
    
    # insert each values tupe into waytag table 
    for inser in waytag:
        try:
            c.execute('insert into waytag (id, k, v) values (?, ?, ?)', inser)
        except sqlite3.IntegrityError:
            pass
        
    # insert each values tupe into waypoint table  
    for inser in waypoint:
        try:
            c.execute('insert into waypoint (wayid, ordinal, nodeid) values (?, ?, ?)', inser)
        except sqlite3.IntegrityError:
            print("Values: " + str(inser) + " violates waypoint constraints.")
            pass            
    
    conn.commit() 
    conn.close()
    
    
    print("Insert into database file successfully!")    
    
main()
