# This program will comput the geographical distance
# between two input nodes in the input database file

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
    # read the database file name
    # node id 1 and node id 2
    database = sys.argv[1]
    point1 = sys.argv[2]
    point2 = sys.argv[3]
    
    # open database file
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    conn.create_function("distance", 4, calculate_distance)
    c = conn.cursor()
    
    # query to compute distace
    c.execute("""SELECT distance(n1.lat, n1.lon, n2.lat, n2.lon) 
    FROM node n1, node n2 
    WHERE n1.id = ? 
    AND n2.id = ?""", (point1, point2))
    
    sol = c.fetchall()
    print("The distance between this two node is: " + str(sol[0][0]) + " km.")
    
    conn.close()
    
main()
