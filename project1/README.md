# Project 1 README:

This program will read the "edmonton.osm" binary map file in XML representation and store the data into database file.    
     
* INSTRUCTION    
     * This program only uses one python file, "project1.py".
     * This program runs both in python2 and python3.    
     * Please put the map data in the same directory with this program file.   
     * When the program terminate, it will print "end" and generate "edmonton.db" file.   
     * While accessing data in "edmonton.db" through sqlite3, please use the "PRAGMA foreign_keys = ON;" to turn on foreign key before updating data.   
     * Constraints will be checked using both foreign key and trigger.    
