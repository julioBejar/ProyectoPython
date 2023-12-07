# https://apuntes.de/python/expresiones-regulares-y-busqueda-de-patrones-en-python-poder-y-flexibilidad/#gsc.tab=0
# https://rico-schmidt.name/pymotw-3/pickle/index.html
# https://stackoverflow.com/questions/55809976/seek-on-pickled-data
# https://www.reddit.com/r/learnpython/comments/pgfj63/sorting_a_table_with_pysimplegui/
# https://www.geeksforgeeks.org/python-sorted-function/
# https://github.com/PySimpleGUI/PySimpleGUI/blob/master/DemoPrograms/Demo_Table_Element_Header_or_Cell_Clicks.py
# https://github.com/PySimpleGUI/PySimpleGUI/issues/5646
# https://docs.python.org/3/howto/sorting.html
import os

from Moto import *
from SerializeFile import *
import PySimpleGUI as sg
import re
import operator
import pandas as pd

# List that will store Moto objects read from the CSV file
l_moto = []

# Definition of regular expression patterns for validation
pattern_id = r"\d{3}+$"
pattern_brand = r"^[A-Za-z]+$"
pattern_year = r"^\d{4}$"  # Pattern for a 4-digit year
pattern_mileage = r"^\d+$"


# Function to add a new moto to the list and save the data to a CSV file
def add_moto(l_moto, t_moto_interface, o_moto, window):
    save_moto('database.csv', l_moto)  # Guardar datos antes de agregar una nueva moto
    l_moto.append(o_moto)  # Agregar el objeto Moto a la lista
    o_moto.pos_file = len(l_moto) - 1
    t_moto_interface.append([o_moto.id, o_moto.brand, o_moto.model, o_moto.year, o_moto.mileage,
                            o_moto.pos_file, o_moto.erased])
    window['-Table-'].update(values=t_moto_interface)

# Function to delete a moto from the list and update the interface and CSV file
def del_moto(l_moto, t_moto_interface, pos_in_table):
    # Read the CSV file and store the data in a DataFrame
    df = pd.read_csv('database.csv')

    # Find the row that has the same ID as the moto to be deleted
    mask = df['id'] == t_moto_interface[pos_in_table][0]

    # If such a row is found, change the value of 'erased' to True
    df.loc[mask, 'erased'] = True

    # Save the DataFrame back to the CSV file
    df.to_csv('database.csv', index=False)

    # Update the list of motos in memory
    for o in l_moto:
        if o.id == t_moto_interface[pos_in_table][0]:
            o.erased = True
            break

    # Remove the moto from the interface's list
    t_moto_interface.remove(t_moto_interface[pos_in_table])

# Function to update a moto in the list and the CSV file
def update_moto(l_moto, t_row_moto_interface, moto_id):
    # Leer el archivo CSV en un DataFrame
    df = pd.read_csv('database.csv')

    # Convertir el ID a cadena antes de la comparación
    moto_id_str = str(moto_id)
    df['id'] = df['id'].astype(str)

    # Identificar la fila que tiene el mismo ID que la moto a actualizar
    mask = df['id'] == moto_id_str

    # Si se encuentra dicha fila, actualizar los valores de esa fila con los nuevos valores de la moto
    if df.loc[mask].shape[0] > 0:
        df.loc[mask, 'brand'] = t_row_moto_interface[1]
        df.loc[mask, 'model'] = t_row_moto_interface[2]
        df.loc[mask, 'year'] = int(t_row_moto_interface[3])
        df.loc[mask, 'mileage'] = int(t_row_moto_interface[4])

        # Guardar el DataFrame actualizado de nuevo en el archivo CSV
        df.to_csv('database.csv', index=False)

        # Actualizar la lista de motos en memoria
        for moto in l_moto:
            if moto.id == moto_id:
                moto.set_moto(t_row_moto_interface[1], t_row_moto_interface[2], t_row_moto_interface[3], t_row_moto_interface[4])
                moto.erased = False  # Asegurarse de que el estado 'erased' esté configurado en False
                break
    else:
        print("Error: No moto with the provided ID was found.")
# Function to handle the event of adding a moto
def handle_add_event(event, values, l_moto, table_data, window):
    validation_errors = []

    # Validate ID
    if not re.match(pattern_id, values['-id-']):
        validation_errors.append("Invalid ID. Must be a 3-digit number.")

    # Validate Brand
    if not re.match(pattern_brand, values['-brand-']):
        validation_errors.append("Invalid Brand. Must contain only letters.")

    # Validate Year
    if not re.match(pattern_year, values['-year-']):
        validation_errors.append("Invalid Year. Must be a 4-digit number.")

    # Validate Mileage
    if not re.match(pattern_mileage, values['-mileage-']):
        validation_errors.append("Invalid Mileage. Must be a non-negative integer.")

    # Check if there are validation errors
    if validation_errors:
        # Display an error message window
        sg.popup_error("Validation Error", "\n".join(validation_errors))
    else:
        # If validation passes, proceed with adding the moto
        add_moto(l_moto, table_data,
                 Moto(values['-id-'], values['-brand-'], values['-model-'], values['-year-'],
                      values['-mileage-'], -1), window)
        window['-Table-'].update(table_data)
# Function to handle the event of deleting a moto
def handle_delete_event(event, values, l_moto, table_data, window):
    if len(values['-Table-']) > 0:
        del_moto(l_moto, table_data, values['-Table-'][0])
        window['-Table-'].update(table_data)

# Function to handle the event of modifying a moto
def handle_modify_event(event, values, l_moto, table_data, window):
    valid = False
    if re.match(pattern_brand, values['-brand-']):
        if re.match(pattern_id, values['-id-']):
            valid = True
    if valid:
        row_to_update = None
        for t in table_data:
            if str(t[0]) == values['-id-']:
                row_to_update = t
                t[1], t[2], t[3], t[4] = values['-brand-'], values['-model-'], values['-year-'], values['-mileage-']
                break
        if row_to_update is None:
            print("Error: No moto with the provided ID was found in the event.")
            return

        # Convertir el valor del ID a un entero
        moto_id = int(values['-id-'])
        update_moto(l_moto, row_to_update, moto_id)
        window['-Table-'].update(table_data)
        window['-id-'].update(disabled=False)

def handle_purge_event(l_moto, table_data, window):
    # Crear un nuevo archivo CSV para los registros eliminados
    deleted_filename = 'deleted_records.csv'

    # Filtrar las motos eliminadas
    deleted_motos = [moto for moto in l_moto if moto.erased]

    # Verificar si hay registros eliminados antes de continuar
    if not deleted_motos:
        print("No hay registros eliminados para purgar.")
        return

    # Crear un DataFrame con las motos eliminadas
    deleted_data = {
        "id": [moto.id for moto in deleted_motos],
        "brand": [moto.brand for moto in deleted_motos],
        "model": [moto.model for moto in deleted_motos],
        "year": [moto.year for moto in deleted_motos],
        "mileage": [moto.mileage for moto in deleted_motos],
        "pos_file": [moto.pos_file for moto in deleted_motos],
        "erased": [moto.erased for moto in deleted_motos],
    }
    deleted_df = pd.DataFrame(deleted_data)

    # Guardar los registros eliminados en el nuevo archivo
    deleted_df.to_csv(deleted_filename, index=False)

    # Eliminar el archivo antiguo solo si existe
    try:
        os.remove('database_deleted.csv')
    except FileNotFoundError:
        pass

    # Renombrar el nuevo archivo solo si existe
    try:
        os.rename(deleted_filename, 'database_deleted.csv')
        print("Registros eliminados purgados exitosamente.")
    except FileNotFoundError:
        print("No hay registros eliminados para purgar.")


# Function to sort the table by multiple columns
def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table

def interface():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('Topanga')
    sg.set_options(font=font1)
    table_data = []
    row_to_update = []
    l_moto = read_moto('database.csv')

    # Fill the data list for the table
    for o in l_moto:
        table_data.append([o.id, o.brand, o.model, o.year, o.mileage, o.pos_file, o.erased])

    # Definition of the interface layout
    layout = [
        [sg.Push(), sg.Text('My Moto Library'), sg.Push()]] + [
        [sg.Text(text), sg.Push(), sg.Input(key=key)] for key, text in Moto.fields.items()] + [
        [sg.Push()] +
        [sg.Button(button) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
        [sg.Push()],
        [sg.Table(values=table_data, headings=Moto.headings, max_col_width=50, num_rows=10,
                  display_row_numbers=False, justification='center', enable_events=True,
                  enable_click_events=True,
                  vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                  expand_x=True, bind_return_key=True, key='-Table-')],
        [sg.Button('Purge'), sg.Push(), sg.Button('Sort File')        ],
    ]
    sg.theme('Topanga')

    # Create the PySimpleGUI window
    window = sg.Window('My Moto Library', layout, finalize=True)

    window['-Table-'].bind("<Double-Button-1>", " Double")

    # Main loop to handle interface events
    while True:
        event, values = window.read()

        # Handle the event of closing the window
        if event == sg.WIN_CLOSED:
            save_moto('database.csv', l_moto)
            break

        # Handle the event of adding a moto
        if event == 'Add':
            handle_add_event(event, values, l_moto, table_data, window)

        # Handle the event of deleting a moto
        if event == 'Delete':
            handle_delete_event(event, values, l_moto, table_data, window)

        # Handle the event of double-clicking on the table
        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-id-'].update(disabled=True)
                window['-id-'].update(str(table_data[row][0]))
                window['-brand-'].update(str(table_data[row][1]))
                window['-model-'].update(str(table_data[row][2]))
                window['-year-'].update(str(table_data[row][3]))
                window['-mileage-'].update(str(table_data[row][4]))
                window['-pos_file-'].update(str(table_data[row][5]))

        # Handle the event of clearing fields
        if event == 'Clear':
            window['-id-'].update(disabled=False)
            window['-id-'].update('')
            window['-brand-'].update('')
            window['-model-'].update('')
            window['-year-'].update('')
            window['-mileage-'].update('')
            window['-pos_file-'].update('')

        # Handle the event of modifying a moto
        if event == 'Modify':
            handle_modify_event(event, values, l_moto, table_data, window)

        # Handle the event of clicking on the table to sort
        if isinstance(event, tuple):
            if event[0] == '-Table-':
                if event[2][0] == -1:  # Header was clicked
                    col_num_clicked = event[2][1]
                    table_data = sort_table(table_data, (col_num_clicked, 0))
                    window['-Table-'].update(table_data)
        if event == 'Purge':
            handle_purge_event(l_moto, table_data, window)


    # Close the window when exiting the loop
    window.close()
# Call the main function
interface()

# Close the file at the end of the program
