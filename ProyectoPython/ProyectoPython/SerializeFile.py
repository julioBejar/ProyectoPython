from Moto import Moto  # Asegúrate de importar la clase Moto adecuada
import pandas as pd

# Función para guardar la lista de motos en un archivo CSV
def save_moto(csv_filename, moto_list):
    moto_data = []
    for moto in moto_list:
        moto_data.append([moto.id, moto.brand, moto.model, moto.year, moto.mileage, moto.pos_file, moto.erased])

    # Crear un DataFrame y guardar en el archivo CSV
    df = pd.DataFrame(moto_data, columns=['id', 'brand', 'model', 'year', 'mileage', 'pos_file', 'erased'])
    df.to_csv(csv_filename, index=False)

# Función para cargar la lista de motos desde un archivo CSV
def read_moto(csv_filename):
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
        return []

    if df is None or df.empty:
        print("Warning: The DataFrame is empty.")
        return []

    moto_list = []
    expected_columns = ['id', 'brand', 'model', 'year', 'mileage', 'pos_file', 'erased']

    # Comprobar la existencia de las columnas esperadas
    missing_columns = [col for col in expected_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: The following columns were not found in the CSV file: {missing_columns}")
        return []

    for index, row in df.iterrows():
        if row['erased'] is False:  # Solo agregar a la lista si 'erased' es False
            moto_list.append(Moto(row['id'], row['brand'], row['model'], row['year'], row['mileage'], row['pos_file'], row['erased']))

    return moto_list
