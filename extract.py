import xlrd
from app import *

sepomex_wb = xlrd.open_workbook("CPdescarga.xls")
hojas = sepomex_wb.nsheets

for i in range(1, hojas):
    values = sepomex_wb.sheet_by_index(i)
    state_name = values.cell(1, 4).value
    capital = values.cell(1, 5).value
    id = values.cell(1, 7).value
    new_state = State(id, state_name, capital)
    db.session.add(new_state)

for i in range(1, hojas):
    sheet = sepomex_wb.sheet_by_index(i)
    for j in range(1, sheet.nrows):
        name = sheet.cell(j, 3)
        state_id = sheet.cell(j, 7).value
        new_municipality = Municipality(name, state_id)
        db.session.add(new_municipality)

for i in range(1, hojas):
    sheet = sepomex_wb.sheet_by_index(i)
    for j in range(1, sheet.nrows):
        postalcode = sheet.cell(j, 0).value
        name_colony = sheet.cell(j, 1).value
        type_colony = sheet.cell(j, 2).value
        type_zone = sheet.cell(j, 13).value
        state_id = sheet.cell(j, 7).value
        new_colony = Colony(postalcode, name_colony, type_colony, type_zone, state_id)
        db.session.add(new_colony)

db.session.commit()
