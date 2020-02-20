# This program will read the edmonton map data(XML format)
# into database

# Schema 
# node (id integer, lat float, lon float)
# way (id integer, closed boolean)
# waypoint (wayid integer, ordinal integer, nodeid integer)
# nodetag (id integer, k text, v text)
# waytag  (id integer, k text, v text)

import xml.etree.ElementTree as ET
import sqlite3

# start XML parse
tree = ET.parse('edmonton.osm')
root = tree.getroot()

# finish XML parse
print("end tree")

db_file_path="./edmonton.db"

# Create or Connect to a Database
conn = sqlite3.connect(db_file_path)
c = conn.cursor()

# Drop tables to avoid error
c.execute('DROP TABLE IF EXISTS node;')
c.execute ('DROP TABLE IF EXISTS way;')
c.execute ('DROP TABLE IF EXISTS waypoint;')
c.execute ('DROP TABLE IF EXISTS nodetag;')
c.execute ('DROP TABLE IF EXISTS waytag;') 


#create table here
c.execute('CREATE TABLE node(id integer,lat float,lon float,PRIMARY KEY (id));')

c.execute('CREATE TABLE way(id integer,closed boolean,PRIMARY KEY (id));')

c.execute("""CREATE TABLE waypoint(wayid integer,ordinal integer,nodeid integer,CHECK (ordinal >= 0),FOREIGN KEY (wayid) 
REFERENCES way(id),
FOREIGN KEY (nodeid) 
REFERENCES node(id) 
ON DELETE CASCADE 
ON UPDATE CASCADE);""")

c.execute("""CREATE TABLE nodetag(id integer,k text,v text,
FOREIGN KEY (id) 
REFERENCES node(id) 
ON DELETE CASCADE
ON UPDATE CASCADE);""")

c.execute("""CREATE TABLE waytag(id integer,k text,v text,
FOREIGN KEY (id) 
REFERENCES way(id) 
ON DELETE CASCADE 
ON UPDATE CASCADE);""")

# Create trigger
# if nodeid is not in node table
# then insert new node to node table
c.execute("""create trigger insert_waypoint
after insert on waypoint
when new.nodeid not in (select n.id from node n where n.id = new.nodeid)
begin
insert into node (id, lat, lon) values (new.nodeid, NULL, NULL);
end;""")



# get node and node tag information 
# store them into node and nodetag table
for node in root.iter('node'):
    n_id = node.get('id')
    lat = node.get('lat')
    lon = node.get('lon')
    
    c.execute("INSERT INTO node VALUES (?,?,?);", (n_id, lat, lon))  
    
    for tag in node.iter("tag"):
        k = tag.get("k")
        v = tag.get("v")
    
        c.execute("INSERT INTO nodetag VALUES (?,?,?);", (n_id, k, v))  


# get way, way point and way tag information 
# store them into way, waypoint and waytag table
for way in root.iter('way'):
    flag = 0
    w_id = way.get('id')
    nd_number = 0
    nd_list = []
    close = False
    inser = []
    
    for subnode in way.iter("nd"):
        ref = subnode.get("ref")
        nd_list.append(subnode.get("ref"))
	inser.append((w_id, nd_number, ref))
	nd_number += 1
        
    # check if the way is closed by checking
    # the first and last node
    if (nd_list[0] == nd_list[nd_number - 1]):
        close = True
        
    c.execute("INSERT INTO way VALUES (?,?);", (w_id, close))  

    for item in inser:
	c.execute("INSERT INTO waypoint VALUES (?,?,?);", item)

    for subnode in way.iter("tag"):
	k = subnode.get("k")
	v = subnode.get("v")
	c.execute("INSERT INTO waytag VALUES (?,?,?);", (w_id, k, v))


# triggers
c.execute("""create trigger insert_waypoint2
        before insert on waypoint
        when new.ordinal -1 != (select max(waypoint.ordinal) from waypoint where waypoint.wayid = new.wayid)
        or new.wayid not in (select way.id from way where way.id)
        begin
        select raise(abort, 'Not ordinal insertion of waypoint!');
        end;""")

c.execute("""create trigger update_waypoint
        after update on waypoint
        when (select nodeid from waypoint where ordinal = (select max(ordinal) from waypoint where wayid = new.wayid)) !=  (select nodeid from waypoint where ordinal = (select min(ordinal) from waypoint where wayid = new.wayid))
        begin
        update way set closed = 0 where id = new.wayid; 
        end;""")

c.execute("""create trigger update_waypoint2
        before update on waypoint
        when old.ordinal != new.ordinal
        begin
        select raise(abort, 'Changing ordinal is not allow. ');
        end;""")

c.execute("""create trigger delete_waypoint
        after delete on waypoint
        when (select closed from way where id = old.wayid) == 1
        begin
        update way set closed = 0 where id = old.wayid; 
        end;""")



# commit and close here
conn.commit()                  
conn.close()
print("end")
    
