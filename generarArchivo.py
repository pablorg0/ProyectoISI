import mysql.connector
import os

config = {
    'host': 'proyectoisiv2-server.postgres.database.azure.com',
    'user': 'uimpsotsiy',
    'password': '8uoyerOVvg9$x2Ru',
    'database': 'proyectoisiv2-database'
}

def write_to_file(file_name, query):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        cursor.execute(query)
        
        # Obtener la ruta absoluta del archivo
        file_path = os.path.join(os.getcwd(), file_name)
        
        with open(file_path, 'w') as f:
            for row in cursor:
                f.write(' \\ '.join(map(str, row)) + '\n')
        print(f"Archivo '{file_name}' creado exitosamente en '{file_path}'")

        cursor.close()
        cnx.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Exception: {e}")

# Queries para obtener los datos
queryWalmart = "SELECT * FROM unlocked_phones"
queryAliexpress = "SELECT * FROM resistant_smartphones"
queryAPI = "SELECT * FROM electronics"

# Crear archivos
write_to_file('productsWalmart.txt', queryWalmart)
write_to_file('productsAliexpress.txt', queryAliexpress)
write_to_file('productsAPI.txt', queryAPI)
