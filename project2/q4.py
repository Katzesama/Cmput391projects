# This program takes as input the database file and
# a list of strings of the form key=value
# then it finds all way elements in the database that 
# have at least one tag matching a key/value combination from the input list
# then compute the length of each way and find the length of the longest way

from math import sin, cos, sqrt, atan2, radians
import sys
import sqlite3

# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
# https://andrew.hedges.name/experiments/haversine/
# function to compute geographical distance
# result returned in km
def calculate_distance (lat1, long1, lat2, long2):
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(lat1)
    lon1 = radians(long1)
    lat2 = radians(lat2)
    lon2 = radians(long2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

# main function here
def main():
    # read and open the input database file
    database = sys.argv[1]
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    conn.create_function("distance", 4, calculate_distance)
    c = conn.cursor()
    
    # read the list of string and find the ways that match
    query = """with get_way(wayid) as( 
    SELECT distinct waytag.id
    FROM waytag
    WHERE"""
    for i in range(2, len(sys.argv)):
        string = sys.argv[i]

        try:
            k, v = string.split('=')    
            if i == len(sys.argv) - 1:
                query = query + " ( k = \"" + k + "\"AND v =\"" + v + "\")"
            else:
                query = query + " ( k = \"" + k + "\"AND v =\"" + v + "\") OR"
                
        except ValueError:
            print("Please input value in a correct format.")
            return        
        
    query = query + """ ) select * from get_way; """
    
    c.execute(query)
    sol = c.fetchall()
    
    # compute the length of each way that we find 
    # and find the number of ways and the the length of the longest way
    query1 = """ with get_node(wayid, nodeid, ord, lat, lon) as(
    SELECT w.wayid, w.nodeid, w.ordinal, node.lat, node.lon
    FROM waypoint w, node
    WHERE w.nodeid = node.id and w.wayid in( """
    for i in range(len(sol)):
        if i == len(sol) - 1:
            query1 = query1 + " (" + str(sol[i][0]) + ")"
        else:
            query1 = query1 + " (" + str(sol[i][0]) + "), " 
    
    query1 = query1 + """)),
    combine_node(wayid, dis) as 
    (select g1.wayid, sum(distance(g1.lat, g1.lon, g2.lat, g2.lon))
    from get_node g1, get_node g2
    where g2.ord = g1.ord + 1 and g1.wayid = g2.wayid
    group by g1.wayid 
    )
    select g.co, max(c.dis)
    from (select count(distinct wayid) as co from get_node) as g, combine_node c
    ;
    """    
    

    c.execute(query1)
    sol = c.fetchall()
    
    print("Number of paths that match the combination is: " + str(sol[0][0]))
    print("Length of longest path is: " + str(sol[0][1]) + " km")
    
    conn.close()
    
main()
