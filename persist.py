import mysql.connector
from datetime import datetime

def insert(placa, orgao, url, descricao,lat, lon):
	now = datetime.now()
	dataEhora = '{}-{}-{} {}:{}:{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)
	mydb = mysql.connector.connect(host='127.0.0.1', user = 'root', passwd = 'aondeja@123', database = 'hackfest')
	mycursor = mydb.cursor()
	insert = "INSERT INTO carros (placa, orgao, url, descricao,latitude,longitude, dataEhora) values ('{}','{}','{}','{}','{}','{}','{}')"
	mycursor.execute(insert.format(placa, orgao, url, descricao,lat, lon, dataEhora))
	mydb.commit()

#data = '{}-{}-{}'.format(now.year, now.month, now.day)
#hora = '{}:{}:{}'.format(now.hour, now.minute, now.second)
#insert = "INSERT INTO carros (placa, orgao, url, descricao, data, hora) values ('{}','{}','{}','{}','{}','{}'')"
#mycursor.execute(insert.format(placa, orgao, url, descricao, data, hora))
