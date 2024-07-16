import requests
from bs4 import BeautifulSoup
import psycopg2
import config  # Archivo config.py que contiene db_config con la configuración de la base de datos

# Conectar a la base de datos PostgreSQL
try:
    db = psycopg2.connect(**config.db_config)
    cursor = db.cursor()
    
    # Crear la tabla si no existe
    cursor.execute("DROP TABLE IF EXISTS resistant_smartphones CASCADE;")
    cursor.execute("""
        CREATE TABLE resistant_smartphones (
            id SERIAL PRIMARY KEY,
            product_id VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            price VARCHAR(255),
            url VARCHAR(255),
            img_url VARCHAR(255)
        );
    """)

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
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page {url}, Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', {'data-component-type': 's-search-result'})
        for product in products:
            try:
                product_id = product.get('data-asin')
                title = product.h2.text.strip()
                link = 'https://www.amazon.de' + product.h2.a['href']
                price = product.find('span', 'a-offscreen').text if product.find('span', 'a-offscreen') else "No price available"
                img_url = product.find('img', 's-image')['src'] if product.find('img', 's-image') else "No image available"
                
                # Insertar en la base de datos
                cursor.execute("""
                    INSERT INTO resistant_smartphones (product_id, name, price, url, img_url)
                    VALUES (%s, %s, %s, %s, %s)
                """, (product_id, title, price, link, img_url))
            except Exception as e:
                print(f"Error procesando producto: {e}")

        db.commit()

    # URL base para scrapear
    base_url = 'https://www.amazon.de/s?k=moviles&crid=QEI48A0RQ340&sprefix=moviles%2Caps%2C179&ref=nb_sb_noss_1'
    
    # Scrapeando la página
    scrape_page(base_url)

    # Cerrar la conexión a la base de datos
    cursor.close()
    db.close()
    print("Conexión cerrada")
except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos", error)
