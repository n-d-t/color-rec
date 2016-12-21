import psycopg2;
import json;
"""
h = dict();
h["wazir"]="halena";
print h;
db = psycopg2.connect(database="colordb", user="analyst", password="enter", host="127.0.0.1", port="5432");
cursor = db.cursor();
print cursor;
t = json.dumps(["halena","hale halena","gazena"])
cursor.execute('INSERT INTO color_set VALUES (%s,%s,%s,%s)',['www.xtnote.com','hello.com',t,234])
db.commit();
cursor.execute('SELECT * FROM color_set;')
print cursor.fetchall();
"""

class DataBase:
    db = {};
    cursor={};
    def __init__(self,database="color", user="analyst", password="enter", host="127.0.0.1", port="5432"):
        
        #establish link to database
        self.db = psycopg2.connect(database=database, user=user, password=password, host=host, port=port);
        self.db.set_isolation_level(0)
    
    #insert into color_set table
    def insert(self,data):
        print data;
        try:
            self.cursor = self.db.cursor();
            sql_st = "INSERT INTO color_set VALUES(%s,%s,%s,%s)";
            self.cursor.execute(sql_st,[data["url"],data["domain"],json.dumps(data["color_data"]),data["ranks"]]);
            self.db.commit();
        except psycopg2.Error , e:
            print "PostGRESql Error ",psycopg2.Error,e.message,e;
            self.db.rollback();
            self.cursor = {};
            
    #fetch from color_set table
    def select(self,start,end):
        self.cursor.execute("SELECT * FROM color_set LIMIT  %s OFFSET %s ",[end,start]);
        result = self.cursor.fetchall()
        return result
        
if __name__ == "__main__":
    d = DataBase();
    p = DataBase();
    data1 = {};
    data1["url"]="www.suchamessi.com/supergoal";
    data1["domain"]="sucha.com";
    data1["color_data"]=["red","blue","green"]
    data1["ranks"]=13242;
    d.insert(data1);
    print p.select(0,1);