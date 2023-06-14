import PySimpleGUI as sg

import os
import sqlite3

# Includes

directory_current = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(directory_current, 'database.db')

connection = sqlite3.connect(db_path)
query = ('''CREATE TABLE IF NOT EXISTS SUPPLIES (LOT CHAR(10), PRODUCT TEXT, SUPPLIER TEXT)''')
connection.execute(query)
connection.close()

###

data = []
Titles = ['Lot', 'Product', 'Supplier']

layout = [
    [sg.Text(Titles[0]), sg.Input(size=10, key=Titles[0])],
    [sg.Text(Titles[1]), sg.Input(size=20, key=Titles[1])],
    [sg.Text(Titles[2]),
     sg.Combo(['Supplier 1', 'Supplier 2', 'Supplier 3'], key=Titles[2])],

    [sg.Button('Add'),
     sg.Button('Edit'),
     sg.Button('Save', disabled=True),
     sg.Button('Delete'),
     sg.Exit('Exit')],

    [sg.Table(data, Titles, key='table')]
]

windows = sg.Window('sistema', layout)

while True:

    event, values = windows.read()
    print(values)

    if event == 'Add':
        data.append([values[Titles[0]], values[Titles[1]], values[Titles[2]]])
        windows['table'].update(values=data)
        for i in range(3):
            windows[Titles[i]].update(value='')

        ### Includes ###
        connection = sqlite3.connect(db_path)
        connection.execute("INSERT INTO SUPPLIES (LOT, PRODUCT, SUPPLIER) VALUES(?, ?, ?)",
                           ([values[Titles[0]], values[Titles[1]], values[Titles[2]]]))
        connection.commit()
        connection.close()

    if event == 'Edit':
        if values['table'] == []:
            sg.popup('No line has been selected')
        else:
            editLine = values['table'][0]
            sg.popup('Edit line selected')
            for i in range(3):
                windows[Titles[i]].update(value=data[editLine][i])
            windows['Save'].update(disabled=False)

    if event == 'Save':
        data[editLine] = [values[Titles[0]],
                          values[Titles[1]], values[Titles[2]]]
        windows['table'].update(values=data)
        for i in range(3):
            windows[Titles[i]].update(value='')
        windows['Save'].update(disabled=True)

        connection = sqlite3.connect(db_path)
        connection.execute("UPDATE SUPPLIES set PRODUCT = ?, SUPPLIER = ? where LOT = ?",
                           ([values[Titles[1]], values[Titles[2]], values[Titles[0]]]))
        connection.commit()
        connection.close()

    if event == 'Delete':
        if values['table'] == []:
            sg.popup('No line has been selected')
        else:
            if sg.popup_ok_cancel("This operation cannot be undone. Confirm?") == "OK":

                connection = sqlite3.connect(db_path)
                connection.execute(
                    "DELETE FROM SUPPLIES WHERE LOT = ?;", (values[Titles[0]],))
                connection.close()

                del data[values['table'][0]]
                windows['table'].update(values=data)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

windows.close()
