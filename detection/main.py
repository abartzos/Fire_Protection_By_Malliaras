import pickle
import sqlite3
import datetime
import serial

location = 'Alimos, Greece'

#starts the serial connection
ser = serial.Serial('/dev/cu.usbmodem14101', 9600)

#a variable for checking if there is a dangerous
#CO percentage in the forest atmosphere (depends on the forest)
CO_threshold = 10

def read_line(connection):
    # reads the line and returns a tuple of the measurements
    line = str(connection.readline())[2:-5]
    #formats the line to a tuple and returns it
    commas = []
    for i in range(len(line)):
        if line[i] == ',':
            commas.append(i)
    return (float(line[:commas[0]]), 
        float(line[commas[0]+1:commas[1]]),
        float(line[commas[1]+1:]))

def check_for_fire(data_tup, classifier, database):
    #checks for fire and uploads
    if classifier.predict(data_tup[0:2][::-1], 5) or data_tup[2] > CO_threshold:
        database.upload(location)

#defines the database class, used later to store data (datetime, loc)
class Database(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self.conn = sqlite3.connect(self.file_name)
    def upload(self, location):
        sql = 'INSERT INTO alerts (datetime,location) VALUES (?,?);'
        cur = self.conn.cursor()
        cur.execute(sql, (str(datetime.datetime.now()), location))
    def close(self):
        self.conn.commit()
        self.conn.close()

with open('classifier', 'rb') as f:
    clf = pickle.load(f)

while True:
    try:
        db = Database('../server/db.db')
        check_for_fire(read_line(ser), clf, db)
        db.close()
    except KeyboardInterrupt:
        break