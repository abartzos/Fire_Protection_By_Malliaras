import pickle
import sqlite3
import datetime

values = [[9,50],'Athens, Greece']

class Database(object):
	def __init__(self, file_name):
		self.file_name = file_name
		self.conn = sqlite3.connect(file_name)
	def upload(self, location):
		self.conn.execute("""INSERT INTO `alerts` (datetime,location)
		 VALUES ('""" + str(datetime.datetime.now()) + "','" + location + "');")
	def close(self):
		self.conn.close()

with open('classifier', 'rb') as f:
    clf = pickle.load(f)

db = Database('../server/db.db')
db.upload(values[1])
db.close()