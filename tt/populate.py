import sqlite3
import datetime
import random
import pudb

def populate():
    BASE_DIR='/root/env/djextjs'
    BASE_DIR='/home/chris/Bureau/DVP/python/django/django-test-extjs'
    conn = sqlite3.connect(BASE_DIR+'/db/data.dbf')
    c = conn.cursor()

    max_enreg = 99
    d = []

    QUI = ( "INTERNE","INTERNE","INTERNE","INTERNE","INTERNE", "CLI001", "CLI002", "CLI003", "FOU01", "FOU02" )
    TEMPS = ( 5, 10, 10, 15, 20, 180, 30 )
    START_DAY = datetime.date( 2013, 6, 1 )

    #pudb.set_trace()

    for i in range(1, max_enreg+1):
        e = (   i, 
                random.choice( QUI ), 
                "libelle court %02d" % i, 
                ## Avec l'heure
                #START_DAY+datetime.timedelta(days=random.choice(range(15)), hours=random.choice(range(6)), minutes=random.choice(range(40))),
                #START_DAY+datetime.timedelta(days=random.choice(range(15))),
                datetime.date( 2013, 6, random.choice(range(28))+1),
                random.choice( TEMPS ), 
                random.choice(("EN_COURS", "FAIT")),
                '<vide>'
            )
        d.append(e)
        

    c.execute("delete from tt_action")
    c.executemany("INSERT INTO tt_action VALUES (?,?,?,?,?,?,?)", d)
    conn.commit()
    conn.close()

def test():
    BASE_DIR='/root/env/djextjs'
    BASE_DIR='/home/chris/Bureau/DVP/python/django/django-test-extjs'
    conn = sqlite3.connect(BASE_DIR+'/db/data.dbf')
    c = conn.cursor()

    c.execute('select * from tt_action where id < 10')
    data = c.fetchall()
    print data

    conn.close()

if __name__ == '__main__':
    populate()
    test()
