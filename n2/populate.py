import sqlite3
BASE_DIR='/root/env/djextjs'
BASE_DIR='/home/chris/Bureau/DVP/python/django/django-test-extjs'
conn = sqlite3.connect(BASE_DIR+'/db/data.dbf')
c = conn.cursor()

max_enreg = 99
d = []

for i in range(1, max_enreg+1):
    e = (   i, 
            "Titre %02d" % i, 
            "Description %02d" % i,
            "TAG1 %02d" % i, 
            "TAG2 %02d" % i, 
            "TAG3 %02d" % i, 
            "TAG4 %02d" % i, 
            "TAG5 %02d" % i, 
            "OK", 
        )
    d.append(e)
    

c.execute("delete from notes_note")
c.executemany("INSERT INTO notes_note VALUES (?,?,?,?,?,?,?,?,?,datetime('now'),datetime('now'))", d)
conn.commit()
conn.close()

#CREATE TABLE "notes_note" (
#        "id" integer NOT NULL PRIMARY KEY,
#        "titre" varchar(50) NOT NULL,
#        "description" text NOT NULL,
#        "tag1" varchar(20) NOT NULL,
#        "tag2" varchar(20) NOT NULL,
#        "tag3" varchar(20) NOT NULL,
#        "tag4" varchar(20) NOT NULL,
#        "tag5" varchar(20) NOT NULL,
#        "status" varchar(5) NOT NULL,
#        "date_cr" datetime NOT NULL,
#        "date_mo" datetime NOT NULL
#);
#
