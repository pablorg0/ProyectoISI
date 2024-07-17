import requests
from bs4 import BeautifulSoup
import psycopg2
import config  # Archivo config.py que contiene db_config con la configuración de la base de datos

# DB setup
try:
    connection = psycopg2.connect(**config.db_config)
    cursor = connection.cursor()

    # Función para crear la tabla si no existe
    def create_table(cursor):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS resistant_smartphones (
            id SERIAL PRIMARY KEY,
            product_id VARCHAR(255) UNIQUE,
            name VARCHAR(255),
            price VARCHAR(255),
            url VARCHAR(255),
            img_url VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        print("Tabla 'resistant_smartphones' creada o ya existe.")

    # Función para insertar productos en la tabla
    def insert_product(cursor, product):
        insert_query = """
        INSERT INTO resistant_smartphones (product_id, name, price, url, img_url)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (product_id) DO UPDATE SET
            name = EXCLUDED.name,
            price = EXCLUDED.price,
            url = EXCLUDED.url,
            img_url = EXCLUDED.img_url
        """
        product_data = (
            product['product_id'],
            product['name'],
            product['price'],
            product['url'],
            product['img_url']
        )
        cursor.execute(insert_query, product_data)
        print(f"Producto {product['product_id']} insertado/actualizado.")

    # Crear la tabla si no existe
    create_table(cursor)

    # Función para scrapear una página
    def scrape_page(url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error al hacer la solicitud: {e}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        if not products:
            print("No se encontraron productos en la página.")
            return
        
        for product in products:
            try:
                product_id = product.get('data-asin')
                if not product_id:
                    continue
                name = product.h2.text.strip()
                link = 'https://www.amazon.de' + product.h2.a['href']
                price = product.find('span', 'a-offscreen').text if product.find('span', 'a-offscreen') else "No price available"
                img_url = product.find('img', 's-image')['src'] if product.find('img', 's-image') else "No image available"
                
                # Insertar en la base de datos
                product_data = {
                    'product_id': product_id,
                    'name': name,
                    'price': price,
                    'url': link,
                    'img_url': img_url
                }
                insert_product(cursor, product_data)
            except Exception as e:
                print(f"Error procesando producto {product.get('data-asin')}: {e}")

        connection.commit()

    # URL base para scrapear
    base_url = 'https://www.amazon.de/s?k=moviles&crid=QEI48A0RQ340&sprefix=moviles%2Caps%2C179&ref=nb_sb_noss_1'
    
    # Scrapeando la página
    scrape_page(base_url)

except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos", error)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Conexión cerrada")
