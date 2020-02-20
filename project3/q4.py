import sys
import sqlite3
import random
import time

# find the number of mbr contained in random generated 
# rectangle and output the average time used to find that
def main():
    total_time = 0
    # set seed for both tree structure
    random.seed(5)
    # read and open the input database file
    database = sys.argv[1]
    
    # read the l and k for size and number of runs
    l = int(sys.argv[2])
    k = int(sys.argv[3])
    
    db_file_path ="./" + database
    conn = sqlite3.connect(db_file_path)
    c = conn.cursor() 
    
    # find the boundary for rectangle that contains all the mbr
    c.execute("""select max(x), max(y) from nodeCartesian;""")
    sol = c.fetchall()
    
    max_x = sol[0][0]
    max_y = sol[0][1]
    
    # k runs
    for i in range(k):
        # generate the size for rectangle
        width = l*random.uniform(1,10)
        height = l*random.uniform(1,10)
        
        in_rectangle = False
        
        # start the timer 
        start = time.time()
        
        # select the bottom left corner for rectangle
        # at least one mbr is in the rectangle
        while in_rectangle == False:
            #this is the bottom left point
            point_bottom_x = random.uniform(0, max_x)
            point_bottom_y = random.uniform(0, max_y)
            
            
            #then calculate 4 points for rectangle and put them into a list. 
            point_upper_x = point_bottom_x + width
            point_upper_y = point_bottom_y + height
            points = [point_bottom_x, point_bottom_y, point_upper_x, point_upper_y]                    
            
            c.execute("""select count(*) from MBR a
            where (a.minX between ? and ?) 
            AND (a.maxX between ? and ?) 
            AND (a.minY between ? and ?) 
            AND (a.maxY between ? and ?);""", (point_bottom_x, point_upper_x, point_bottom_x, point_upper_x, point_bottom_y, point_upper_y, point_bottom_y, point_upper_y))
            sol = c.fetchall()    
            
            if int(sol[0][0]) > 0:
                in_rectangle = True
            
        
        # find the number of mbrs in rectangle
        c.execute("""select count(*) from MBR a
        where (a.minX between ? and ?) 
        AND (a.maxX between ? and ?) 
        AND (a.minY between ? and ?) 
        AND (a.maxY between ? and ?);""", (point_bottom_x, point_upper_x, point_bottom_x, point_upper_x, point_bottom_y, point_upper_y, point_bottom_y, point_upper_y))

        sol = c.fetchall()
        
        end = time.time()
        run = end - start
        total_time = total_time + run
    # calculate and output the average time over k runs 
    avg = total_time/k
    
    print(str(k) + "\t" + str(l) + "\t" + str(avg))
    conn.close()
    
    
main()    
