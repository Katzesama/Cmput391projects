import sys
import sqlite3
from math import sin, cos, sqrt, atan2, radians

def main():
    # read and open the input database file
    database = sys.argv[1]
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor() 

    # find all the node's x and y value in a waypoint(closed)
    # then select the min(x) max(x) min(y) max(y) as two end point
    # for mbr
    print("create table areaMBR(id integer, minX float, maxX float, minY float, maxY float, PRIMARY KEY(id));")
    c.execute("""select way.id, min(n.x), max(n.x), min(n.y), max(n.y) 
    from nodeCartesian n, way, waypoint w
    where w.nodeid = n.id and way.id = w.wayid and way.closed = 1
    group by way.id;""")
    sol = c.fetchall()
    
    # query to insert
    query = "insert into areaMBR(id, minX, maxX, minY, maxY) values "
    for i, s in enumerate(sol):
        query += str(s)
        if i < len(sol) - 1:
            query += ","
            
    query += ";"
    print(query) 
    
    conn.close()
    
    
main()
