import sys
import sqlite3
import math
import ast


#Global variables: 
#make db and cursor global, because this program will not change database. 
#read and open the input database file
database = sys.argv[1]
x = int(sys.argv[2])
y = int(sys.argv[3])
k = int(sys.argv[4])

point = [x, y]

db_file_path ="./" + database
conn = sqlite3.connect(db_file_path)
c = conn.cursor() 

#make id list and distance global, this is easier for compair distance and update inside function. 
#after this program calculate distance, it will update and sort all nodes in list. 
#this list will store distance of areaMBR and it's id. 
#each element in nearest_out list has format: [distance, id]
nearest_out = [[float("inf"),-1]]*k


# this will do the upward pruning to prune the branchlist
# compare the distance of object and node's mindist
def UpwardPruning(infoList):
    cut_list = []
    max_nearest = nearest_out[k-1][0]
    for i in range(len(infoList)):
        if infoList[i][1] >= max_nearest:
            pass
        else:
            cut_list.append(infoList[i])
    return cut_list
        
#this function will take a list of nodeno as branchList and node info
# as info to sort it base ordering in metric value and return list of nodeno after sorting. 
def SortCalMetricValues(info):
    #nodeinfo has format: [id, minX, maxX, minY, maxY]
    #each item in infoList has format[nodeinfo, mindist, minimaxDist]
    infoList = []
    for item in info:
        infoList.append([item, float('inf'), float('inf')])
    
    for i in range(len(infoList)):
        
        #nodeinfo has format: [id, minX, maxX, minY, maxY]
        mindist = 0
        #minmax will calculate in later part. 
        
        #calculate mindist by algorithm
        #use Sx and Tx, conpare with Px
        rx = 0
        Sx = infoList[i][0][1]
        Tx = infoList[i][0][2]
        #by algorithm
        if point[0] < Sx:
            rx = Sx
        elif point[0] > Tx:
            rx = Tx   
        else:
            rx = point[0]
        
        #use Sy and Ty, compare with Py
        ry = 0
        Sy = infoList[i][0][3]
        Ty = infoList[i][0][4]
        
        #by algorithm
        if point[1] < Sy:
            ry  = Sy
        elif point[1] > Ty:
            ry  = Ty   
        else:
            ry = point[1]     
            
        mindist = (point[0]-rx)**2 + (point[1]-ry)**2
        
        #assign mindist into infoList
        infoList[i][1] = mindist
            
        #calculate minmaxDist by algorithm
        #calculate rmx
        rmx = 0
        if point[0] <= (Sx + Tx)/2:
            rmx = Sx
        else:
            rmx = Tx
        #calculate rmy
        rmy = 0
        if point[1] <= (Sy + Ty)/2:
            rmy = Sy
        else:
            rmy = Ty
        
        #calculate |pk-rmk|^2, name it into minmax_upper
        minmax_upperx = (point[0] - rmx)**2
        minmax_uppery = (point[1] - rmy)**2
        
        #calculate rMi by algorithm
        rMx = 0
        if point[0] >= (Sx + Tx)/2:
            rMx = Sx
        else:
            rMx = Tx
        
        #calculate rmy
        rMy = 0
        if point[1] >= (Sy + Ty)/2:
            rMy = Sy
        else:
            rMy = Ty        
        #calculate sigma |pi-rMi|^2, name it into minmax_lower
        minmax_lowerx = (point[0] - rMx)**2
        minmax_lowery = (point[1] - rMy)**2
        minmax_lower = minmax_lowerx + minmax_lowery
        
        #calculate 2 possiblity of minmaxDist and select min
        minmaxDist1 = minmax_upperx + minmax_lower
        minmaxDist2 = minmax_uppery + minmax_lower
        
        #each item in infoList has format[nodeinfo, mindist, minimaxDist]
        #put minmax in list. 
        if minmaxDist1 >= minmaxDist2:
            infoList[i][2] = minmaxDist2
        else:
            infoList[i][2] = minmaxDist1

    #after calculate infoList, need to sort and return.
    #sort list by minDist. 
    infoList.sort( key=lambda nodes: nodes[2])
      
    branchList = []
    #MBR Ri with MINDIST(P,Ri) >= MINMAXDIST(P,Rj) can be pruned.
    
    for j in range(len(infoList)):
        if infoList[j][1] < infoList[0][2]:
            branchList.append(infoList[j])
                
            
    branchList.sort( key=lambda nodes: nodes[1])
    
    #each item in infoList has format[nodeinfo, mindist, minimaxDist]
    
    pos = 0
    shift = False
    for i in range(k):
        if nearest_out[i][0] >= infoList[0][2]:
            pos = i
            shift = True
            break
        
    if shift:
        for j in range(pos, k):
            nearest_out[j] = [float("inf"),-1]
            
    return branchList


#NearestNeighborSearch is the algorithm using recursive call
#Node is nodeid, point is initial positon, nearset in paper of algrithm 
#is not needed, because this program is finding K nearest area. 
def NearestNeighborSearch(Node):
    branchList = []
    c.execute( """select count(*) from  MBR_parent p where p.parentnode = ?;""", (Node,))
    sol = c.fetchall()  
    
    #if node is not parent, it is leaf.
    count = sol[0][0]
    
    #base case when node is leaf. Then calculate leaf and update buffer.
    if count == 0:
        c.execute("""select a.id, a.minX, a.maxX, a.minY, a.maxY from MBR_rowid r, areaMBR a where a.id = r.rowid and r.nodeno =? group by a.id;""", (Node,))
        sol = c.fetchall()

        for i in range(len(sol)):
            #find midpoint for the areaMBR. Use this point for DIST(P,O)
            midpoint = [(sol[i][2]+sol[i][1])/2,(sol[i][4]+sol[i][3])/2]
            
            dist = math.sqrt((point[0] - midpoint[0])**2 + (point[1] - midpoint[1])**2)
    
            #insert node in correct position. 
            for j in range(k):
                if dist < nearest_out[j][0]:
                    nearest_out.insert(j, [dist,sol[i][0]])
                    nearest_out.pop()
                    break      
        return
        
            
    #this node is a parent node, need to go deeper. 
    else:   
        #sort branch list on order of metric values
        #get all child nodes info here. 
        #node will sort according child_info. 
        c.execute("""select rtreenode(2,data) from MBR_node where nodeno = ?;""", (Node,))
        data = c.fetchall()[0][0]
        data = [float(i) for i in data.replace('{', '').replace('}', '').replace(' ', ',').split(',')]
        
        child_info = []
        tempLine = []
        j = 0
        
        for i in range(len(data)):
            if j < 5:
                tempLine.append(data[i])
                j = j + 1
            if j == 5:
                j = 0
                child_info.append(tempLine)
                tempLine = []
    
        #list sort in here. 
        branchList = SortCalMetricValues(child_info)
        
        #for every item in branchList, do recursion
        for node in branchList:
            NearestNeighborSearch(node[0][0])
            
            #If MINDIST(P,R) >= DIST(P,O) for and MBR R and object O, R can be pruned since it cannot contain an object closer to P than O.
            branchList = UpwardPruning(branchList)
            
        branchList = []  

# main function here to start
def main():
    #pass root node into NearestNeighborSearch
    root = 1
    NearestNeighborSearch(root)
    
    #print out id and distance
    for i in range(len(nearest_out)):
        print("id: " + str(nearest_out[i][1]) + " distance: " + str(nearest_out[i][0]))
        
main()
