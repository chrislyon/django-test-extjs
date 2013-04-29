import sqlite3
BASE_DIR='/root/env/djextjs'
conn = sqlite3.connect(BASE_DIR+'/db/data.dbf')
c = conn.cursor()

max_enreg = 99
d = []

for i in range(1, max_enreg+1):
    e = ( i, "COD%02d" % i, "Nom contact %02d" % i, "Description ", "060000%02d" % i, 'PRO' )
    d.append(e)
    

c.execute("delete from contact_contact")
c.executemany('INSERT INTO contact_contact VALUES (?,?,?,?,?,?)', d)
conn.commit()
conn.close()

## Zones
#"id" integer NOT NULL PRIMARY KEY,
#"cod_contact" varchar(20) NOT NULL UNIQUE,
#"nom_contact" varchar(40) NOT NULL,
#"description" text NOT NULL,
#"tel_contact" varchar(30) NOT NULL,
#"typ_contact" varchar(10) NOT NULL

