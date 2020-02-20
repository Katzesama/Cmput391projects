import sys
import sqlite3
from math import sin, cos, sqrt, atan2, radians

# value used to convert lon: 67137
# lat: 111286
def main():
    # read and open the input database file
    database = sys.argv[1]
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor() 
    
    # select the minimum lat and lon as original point
    c.execute("select min(lat) from node;")
    soll = c.fetchall()
   
    c.execute("select min(lon) from node;")
    sol = c.fetchall()

    orix = sol[0][0]
    oriy = soll[0][0]
    
    # query to create table
    print("create table nodeCartesian(id integer, x float, y float, PRIMARY KEY(id));")
    
    c.execute("select * from node;")
    sol1 = c.fetchall()
    
    # query to insert other node
    # find the node lon and lat and then convert them
    query = "insert into nodeCartesian(id, x, y) values "
    for i, s in enumerate(sol1):
        n_id = s[0]
        x = (s[2] - orix) * 67137
        y = (s[1] - oriy) * 111286      
        intuple = (n_id, x, y)
        query += str(intuple)
        if i < len(sol1) - 1:
            query += ","
    query += ";"
    print(query)
    
    conn.close()
    
    
main()
