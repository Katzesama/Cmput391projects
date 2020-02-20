# This program takes as input a database file 
# and a tsv file that each lines contains a node element. 
# Then it will read the tsv file and insert the node element
# into database file accordingly.

import csv
import sqlite3
import sys

# main function 
def main():
    # read the input database file and tsv file
    database = sys.argv[1]
    file_name = sys.argv[2]
    
    # open the database file
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor()
    
    c.execute("PRAGMA foreign_keys = on")
    
    # open the tsv file and read each line
    with open(file_name) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        i = 0
        
        # list of values to be inserted into database file later
        node_inser = []
        tag_inser = []
        
        for row in rd:
            # if a line has less than 3 columns
            if len(row) < 3:
                print('Please make sure the input tsv file has a least three columns.')
                return
            
            # read the node id, lat, and lon
            tuple_node = ()
            for i in range(0, 3):
                tuple_node = tuple_node + (row[i],)
                try:
                    float(row[i])
                except ValueError:
                    print("Please make sure the input tsv file at least contian 'node', 'lat', 'lon'.")
                    return     
                
            node_inser.append(tuple_node)
            
            # start to read the value for nodetag
            if len(row) > 3:
                tuple_tag = ()
                for i in range(3, len(row)):
                    try:
                        k, v = row[i].split('=')
                    except ValueError:
                        print("Please make sure nodetag is in format 'k = v'.")
                        return
                    
                    tuple_tag += (row[0],)
                    tuple_tag += (k,)
                    tuple_tag += (v,)
                tag_inser.append(tuple_tag)
   
    # insert each values tupe into node table
    for inser in node_inser:
        try:
            c.execute('insert into node (id, lat, lon) values (?, ?, ?)', inser)
        except sqlite3.IntegrityError:
            print("Node: " + inser[0] + " already exist.")
            pass
    
    # insert each values tupe into nodetag table
    for inser in tag_inser:
        try:
            c.execute('insert into nodetag (id, k, v) values (?, ?, ?)', inser)
        except sqlite3.IntegrityError:
            pass        
    
    conn.commit() 
    conn.close()
    
    
    print("Insert into database file successfully!")
    
main()
