# This program will take input database file and a list of strings
# compute the geographic distance between each node in the database file
# that have at least one tag matching a key/value combination from the input list
# and find the largest pairwise distance among those nodes

from math import sin, cos, sqrt, atan2, radians
import sys
import sqlite3
import re

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
    
    # read the list of string and find the nodes that match
    query = """with get_node(id) as ( 
    SELECT distinct nodetag.id
    FROM nodetag
    WHERE"""
    for i in range(2, len(sys.argv)):
        string = sys.argv[i]

        try:
            k, v = string.split('=')    
            if i == len(sys.argv) - 1:
                query = query + " ( nodetag.k = \"" + k + "\"AND nodetag.v =\"" + v + "\")"
            else:
                query = query + " ( nodetag.k = \"" + k + "\"AND nodetag.v =\"" + v + "\") OR"
                
        except ValueError:
            print("Please input value in a correct format.")
            return        

    query = query +  """) select * from get_node;"""
    c.execute(query)
    sol = c.fetchall()
    
    # compute the distance of each pair of nodes that we find 
    # and find the number of nodes and the largest pairwise distance
    query1 = """ with node_l(nodeid, lat, lon) as (
    select distinct node.id, node.lat, node.lon
    from node
    where node.id in ("""
    
    for i in range(len(sol)):
        if i == len(sol) - 1:
            query1 = query1 + " (" + str(sol[i][0]) + ")"
        else:
            query1 = query1 + " (" + str(sol[i][0]) + "), "       
    
    query1 = query1 + """)),
    combine_node(dis) as 
    (select distance(g1.lat, g1.lon, g2.lat, g2.lon)
    from node_l g1, node_l g2
    where g1.nodeid > g2.nodeid)
    select max(cn.dis), g.c
    from combine_node cn, (select count(node_l.nodeid) as c from node_l) as g; """
    
    c.execute(query1)
    sol = c.fetchall()

    # print solution
    print("Number of node found : " + str(sol[0][1]))
    print("Max distcance is: " + str(sol[0][0]) + " km")
             
    conn.close()        
   
main()
