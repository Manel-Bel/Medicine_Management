import sqlite3
import os

DB_NAME = 'Medoc.db'
def create_table():
    cnx= sqlite3.connect(DB_NAME)
    cursor= cnx.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS Medoc(
                        photo BLOB,
                        id TEXT PRIMARY KEY,
                        description STRING,
                        date STRING,
                        quantite INTEGER)""")
    
    cnx.commit()
    cnx.close()

def get_all():
    cnx = sqlite3.connect(DB_NAME)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM Medoc')
    medoc = cursor.fetchall()
    cnx.close()
    return medoc

def insertion(nom,photo,description,date,quantite):
    photo =convert_to_binary(the_file=photo)
    cnx = sqlite3.connect(DB_NAME)
    cursor = cnx.cursor()
    cursor.execute('INSERT INTO Medoc (photo,id,description,date,quantite) VALUES (?,?,?,?,?)',(photo,nom,description,date,quantite))
    print("insertion db done")
    cnx.commit()
    cnx.close()

def supprimer(id):
    cnx = sqlite3.connect(DB_NAME)
    cursor = cnx.cursor()
    cursor.execute('DELETE FROM Medoc WHERE id = ?',(id,))
    cnx.commit()
    cnx.close()


def existe_deja(id):
    cnx = sqlite3.connect(DB_NAME)
    cursor = cnx.cursor()
    cursor.execute('SELECT COUNT(*) FROM Medoc WHERE id=?',(id,))
    r = cursor.fetchone()
    cnx.close()
    return r[0] > 0

def recherche(id):
    cnx = sqlite3.connect(DB_NAME)
    cursor = cnx.cursor()
    cursor.execute('SELECT * FROM Medoc WHERE id=?',(id,))
    r = cursor.fetchone()
    cnx.close()
    return r

def convert_to_binary(the_file):
        dest= None
        with open(the_file, 'rb') as file:
            dest = file.read()
        return dest
        