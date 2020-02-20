# Project 2 README:

* About the DISTANCE FUNCTION:   
        Even though database provides the longtitude and latitude(coordinates) of each node, Earth is not a flat surface   
        and we cannot use the formula like delta(y) / delta(x). So we should treat earth like a sphere object. Therefore,   
        we use Haversine formula which can handle the calculation of any two points's shortest distance on sephere.   
        It uses the radius of Earth(6373 km), longtitude and latitude of the two points.
       
        Distance calculation base on formula on this page: https://andrew.hedges.name/experiments/haversine/
        distance function reference: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude    
        
* INSTRUCTION:   
    
    MUST DO! Please put database files, tsv files and python program files in same directory.   
    Example schema for database file:      
        CREATE TABLE node(id int, lat float, lon float, primary key(id));    
        CREATE TABLE way(id int, closed boolean, primary key(id));     
        CREATE TABLE waypoint(wayid int, ordinal int, nodeid int, foreign key(wayid) references way(id), foreign key(nodeid)   
        references node(id) check(ordinal>=0));    
        CREATE TABLE nodetag(id int, k char(100), v char(100), foreign key(id) references node(id));    
        CREATE TABLE waytag(id int, k char(100), v char(100), foreign key(id) references way(id));    
  
  * Q1(q1.py):      
             1. This program takes database file and two nodes identifier.      
             2. Then it will use the node's latitude and longtitude to calculate the geographical distance between 2 nodes in    
                km.    
             3. If the input nodes are in the database file, it will output the values in float otherwise "None".     
             4. For calculation, it uses a new SQL function called from a user define function in q1.py code.      
               
             command line to run example: python q1.py <db_name> <point1_id> <point2_id>    
                                     i.e. python q1.py edmonton.db 29770958 29770959     
                                    
                                      
  * Q2(q2.py):         
            1. This program will take a database file and a list of string. Each string should be in the form of "key=value".     
            2. Key is "k" value in nodetag table, value is "v" value in nodetag table.     
            3. Then it will find the nodes in database file that have at least one tag matching a key/value combination from  
            the input list.    
            4. It will use the distance function in q1.py to compute the distance for every pair of all the nodes found.    
            5. Then it will print out the number of nodes found and maximum pairwise distance among those nodes in km.   
            6. If no nodes found, it will print the values as "None".   
            Note: This program takes at most 100 key=value pairs.     

            command line to run example: python q2.py <db_name> <key1=value1> <key2=value2> <key3=value3> ...
                                    i.e. python q2.py edmonton.db ele=645 name=Edmonton
  
  * Q3(q3.py):    
            1. This program takes in a database file and a way identifier.    
            2. Then it will find the way element in the database that matches the way id.    
            3. Once the way found, it will use the nodes in the waypoint table and use the q1.py distance function to    
            compute the distance between each neighbour nodes in way point table.   
            4. Finally, it will sum up all the distance from step 3 and out put the value as length of the way.   
            5. If the way id is not in database, then it will output the value as "None".     
    
            command line to run example: python q3.py <db_name> <wayid>    
                                    i.e. python q3.py edmonton.db 4734663


  * Q4(q4.py):      
            1. This program will take in a database file and a list of string in the form "key=value".    
            2. Key is "k" value in waytag table, value is "v" value in waytag table.   
            3. It will find the way element in the database that have at least one tag matching a key/value combination   
            from the input list.    
            4. It will use the similar way in q3.py to compute each way's length.    
            5. Finally, it will print out the number of ways found and the maximum length among these ways.   
            6. If no way was found, it will output the values as "None".     
            Note: This program takes at most 100 key=value pairs.     

            command line to run example: python q4.py <db_name> <key1=value1> <key2=value2> <key3=value3> ...
                                    i.e. python q4.py edmonton.db highway=primary lanes=2 maxheight=5.5


  * Q5(q5.py):    
            tsv file example: node.tsv (it is contained in this branch).     
            1. This program will take a database file and a tsv file contains node information.      
            2. In that file, each node must be described by at least three columns(to be inserted into node table):       
            (0) the node id;    
            (1) the latitude;    
            (2) the longitude.     
            3. tsv file can have more colums to describe the tag of node, it must have format key=value(to be inserted    
            into nodetag table).      
            4. If it identifies the tsv file is not in correct format, it will stop processing and return an error message.   
            5. Otherwise it will read all the node element in tsv file and insert it into the database file accordingly.  
            Note: While inserting, if some constrains in database file are violated, the value will not be inserted and   
            an error message will be printed. But program will still continue process the rest of values.     

            command line to run example: python q5.py <db_name> <tsv_filename>
                                    i.e. python q5.py edmonton.db node.tsv


  * Q6(q6.py):    
            tsv file example: way.tsv (it is contained in this branch).      
            1. This program will take a database file and a tsv file contains way element.    
            2. In that file, each way must be described by two consecutive non-blank lines:      
             The first such line has the id of the way in column 0(to be inserted into way table), followed by zero or more   
             strings of the form key=value in subsequent columns, with tags for the way(to be inserted into waytag table).      
             The second line has all the nodes (identifiers) in the way, with the column number corresponding     
             to the order of the node(to be inserted into waypoint).    
            3. Then it will start to read the tsv file. If it identifies the tsv file is not in correct format,    
            it will stop processing and return an error message.     
            4. Otherwise it will read all the way element in tsv file and insert it into the database file accordingly.  
            Note: While inserting, if some constrains in database file are violated, the value will not be inserted and   
            an error message will be printed. But program will still continue process the rest of values.     

            command line to run example: python q6.py <db_name> <tsv_filename>
                                    i.e. python q6.py edmonton.db way.tsv
