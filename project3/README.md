# Project 3 README:

* INSTRUCTION:   
    
    MUST DO! Please put database files and python program files in same directory.   
    Please use Edmonton's data.
    Example schema for database file:      
        CREATE TABLE node(id int, lat float, lon float, primary key(id));    
        CREATE TABLE way(id int, closed boolean, primary key(id));     
        CREATE TABLE waypoint(wayid int, ordinal int, nodeid int, foreign key(wayid) references way(id), foreign key(nodeid)   
        references node(id) check(ordinal>=0));    
        CREATE TABLE nodetag(id int, k char(100), v char(100), foreign key(id) references node(id));    
        CREATE TABLE waytag(id int, k char(100), v char(100), foreign key(id) references way(id));
  
  * Q1(q1.py):      
             1. This program takes database file.      
             2. Then it will use the node's latitude and longtitude in the database and convert them to y and x in
                meters.    
             3. It will output some query to create table nodeCartesian(id, x, y) to store the id and the Cartesian    
             coordinates that coverts from node's lon and lat.     
             4. Finally, use the command line to put the table and value into unit3q1.db(another database file).      
               
             command line to run example: 
                                         % cp edmonton.db unit3q1.db    
                                         % python q1.py edmonton.db > q1_output    
                                         % sqlite3 unit3q1.db < q1_output
                                    
                                      
  * Q2(q2.py):         
             1. This program takes database file.      
             2. Then it will use the node's x and y value from q1 to find the MBR for each closed way.
             3. It will output some query to create table areaMBR(id, minX, maxX, minY, maxY) to store the id of way    
             and the Cartesian coordinates of the minimum bounding rectangle of every closed way in the input database.   
             coordinates that coverts from node's lon and lat.     
             4. Finally, use the command line to put the table and value into unit3q2.db(another database file).     

            command line to run example: % cp unit3q1.db unit3q2.db    
                                         % python q2.py unit3q1.db > q2_output    
                                         % sqlite3 unit3q2.db < q2_output
  
  * Q3(q3.md):    
            1. Please follow the command line in q3.md. It will create two types of index tree on table areaMBR.   

  * Q4(q4.py, q4.md):      
            1. This program will take in a database(with index tree) file and parameter of l and k.    
            2. In each k run, it will randomly genrate a rectangle with width l*rand(1,10) and heightl*rand(1,10).   
            3. Timer starts. Then randomly find the bottom left corner point for the rectangle(rectangle must contain at least 
            one MBR from areaMBR table).  
            4. It will find the number of MBRs that are in the rectangle and the time elapsed is recored.    
            5. Finally, it will output the average time used to find the number of MBR over k runs.  
            6. The output is in format: k, l and average execution time of the queries, they are seperated by tabs.
            Note: see q4.md for report.

            command line to run example: python q4.py <db_name> l k
                                    i.e. python q4.py unit3q3_btree.sql 25 100


  * Q5(q5.py):       
            1. This program will take a database file like unit3q3_rtree.sql created as in Q3, coordinates x, y    
            and parameter k.           
            2. Then it will find the k areas (in areaMBR) that are closest to query point (x,y).               
            3. The program will output the id of area and the distance to point(x,y) in increasing order.    

            command line to run example: python q5.py <db_name> x y k 
                                    i.e. python q5.py unit3q3_rtree.db 100 200 10
