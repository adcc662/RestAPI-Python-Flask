import pymysql

pymysql.install_as_MySQLdb()
import MySQLdb
import xlrd

sepomex_wb = xlrd.open_workbook("CPdescarga.xls")
database = MySQLdb.connect(host="localhost", user="root", passwd="", db="sepomex_beta")
hojas = sepomex_wb.nsheets
cursor = database.cursor()

query_estados = """INSERT INTO state(name_state, capital)"""

for i in range(1, hojas.nrows):
    name_state = hojas.cell(i, 4)
    capital = hojas.cell(i, 4)

query_municipios = """INSERT INTO municipality(name)"""
for j in range(1, hojas.nrows):
    name = hojas.cell(j, 3)

query_colony = """INSERT INTO colony(postalcode, name_colony, type_colony, type_zone)"""
for r in range(1, hojas.nrows):
    postalcode = hojas.cell(r, 6)
    name_colony = hojas.cell(r, 1)
    type_colony = hojas.cell(r, 2)
    type_zone = hojas.cell(r, 13)


