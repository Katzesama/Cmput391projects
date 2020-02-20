# This program takes as the database file and 
# the identifier of a way element in the database
# and compute the length of the way element

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
    # read the database file and way id
    database = sys.argv[1]
    wayid = sys.argv[2]
    
    # open the database file
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    conn.create_function("distance", 4, calculate_distance)
    c = conn.cursor()
    
    # get all the node that is in the waypoint of the input way
    query = """with get_node(id, ord, lat, lon) as(
    SELECT waypoint.nodeid, waypoint.ordinal, node.lat, node.lon
    FROM waypoint, node
    WHERE waypoint.wayid =""" + wayid
    
    # comput the distace of each neighbour nodes first
    # then sum them and output the lenght of the way
    query = query + """ and node.id = waypoint.nodeid),
    combine_node(id1, id2, dis) as 
    (select g1.id, g2.id, distance(g1.lat, g1.lon, g2.lat, g2.lon)
    from get_node g1, get_node g2
    where g1.ord = g2.ord - 1)
    select sum(c.dis)
    from combine_node c
    ;
    """
    
    c.execute(query)
    length = c.fetchall()
        
    print("The length of the way is: " + str(length[0][0]) + " km")
    
    conn.close()
    
main()
