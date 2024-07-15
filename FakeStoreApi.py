import requests
import re
import config
import mysql.connector

# DB setup
db = mysql.connector.connect(**config.db_config)
cursor = db.cursor()

# Función para crear la tabla si no existe
def create_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS electronics (
        id INT PRIMARY KEY,
        name VARCHAR(255),
        price DECIMAL(10, 2),
        description TEXT,
        category VARCHAR(255),
        image TEXT,
        url VARCHAR(255)
    )
    """
    cursor.execute(create_table_query)

# Función para insertar productos en la tabla
def insert_product(cursor, product):
    insert_query = """
    INSERT INTO electronics (id, name, price, description, category, image, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        price = VALUES(price),
        description = VALUES(description),
        category = VALUES(category),
        image = VALUES(image),
        url = VALUES(url)
    """
    product_data = (
        product['id'],
        product['tittle'],
        product['price'],
        product['description'],
        product['category'],
        product['image'],
        product['url']
    )
    cursor.execute(insert_query, product_data)

# URL de la API de Fakestoreapi para la categoría "electronics"
url = "https://fakestoreapi.com/products/category/electronics"

try:
    # Hacer una solicitud GET a la API
    response = requests.get(url)
    response.raise_for_status()

    # Obtener los datos en formato JSON
    electronics_products = response.json()

    # Conectar a la base de datos
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        cursor = connection.cursor()
        # Crear la tabla si no existe
        create_table(cursor)
        
        # Insertar cada producto en la tabla
        for product in electronics_products:
            product['url'] = url
            insert_product(cursor, product)
        
        # Confirmar los cambios
        connection.commit()
        print("Datos insertados correctamente en la tabla 'electronics'.")

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Error as db_err:
    print(f"Database error occurred: {db_err}")
except Exception as err:
    print(f"An error occurred: {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()



##Codigo "extra" si hiciese falta usar tokens

# # Función para obtener el token de acceso
# def get_access_token():
#     auth_url = "https://example.com/api/token"
#     auth_data = {
#         'grant_type': 'client_credentials',
#         'client_id': 'tu_client_id',
#         'client_secret': 'tu_client_secret'
#     }
#     response = requests.post(auth_url, data=auth_data)
#     response.raise_for_status()
#     return response.json()['access_token']

# # URL de la API para la categoría "electronics"
# url = "https://example.com/api/products/category/electronics"

# try:
#     # Obtener el token de acceso
#     access_token = get_access_token()
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }

#     # Hacer una solicitud GET a la API
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()

#     # Obtener los datos en formato JSON
#     electronics_products = response.json()

#     # Conectar a la base de datos
#     connection = mysql.connector.connect(**db_config)
#     if connection.is_connected():
#         cursor = connection.cursor()
#         # Crear la tabla si no existe
#         create_table(cursor)
        
#         # Insertar cada producto en la tabla
#         for product in electronics_products:
#             insert_product(cursor, product)
        
#         # Confirmar los cambios
#         connection.commit()
#         print("Datos insertados correctamente en la tabla 'electronics'.")

# except requests.exceptions.HTTPError as http_err:
#     print(f"HTTP error occurred: {http_err}")
# except Error as db_err:
#     print(f"Database error occurred: {db_err}")
# except Exception as err:
#     print(f"An error occurred: {err}")
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         cursor.close()
#         connection.close()
