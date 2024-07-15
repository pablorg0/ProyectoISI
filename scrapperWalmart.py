import requests
from bs4 import BeautifulSoup
import psycopg2
import time
import config  # Archivo config.py que contiene db_config con la configuración de la base de datos

# Conexión a la base de datos PostgreSQL
try:
    db = psycopg2.connect(**config.db_config)
    cursor = db.cursor()

    # Crear la tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unlocked_phones (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2),
            url VARCHAR(255),
            img_url VARCHAR(255)
        );
    """)
    db.commit()

    # Función para scrapear una página
    def scrape_page(url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Unable to fetch page {url}")
            return
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.find_all('div', class_='search-result-gridview-item-wrapper')
        for product in products:
            name_tag = product.find('a', class_='product-title-link')
            if not name_tag:
                continue
            
            name = name_tag.text.strip()
            link = 'https://www.walmart.com' + name_tag['href']
            
            price_tag = product.find('span', class_='price-main')
            if price_tag:
                price_text = price_tag.find('span', class_='visuallyhidden').text.strip()
                price = float(price_text.replace('$', '').replace(',', ''))

            img_tag = product.find('img', class_='search-result-productimage')
            img_url = img_tag['src'] if img_tag else None
            
            # Insertar en la base de datos
            cursor.execute("""
                INSERT INTO unlocked_phones (name, price, url, img_url)
                VALUES (%s, %s, %s, %s)
            """, (name, price, link, img_url))

        db.commit()

    # Scrapeando las páginas de la 1 a la 25
    base_url = 'https://www.walmart.com/browse/unlocked-phones/1105910_1073085?povid=web_categorypage_cellphones_lefthandnav'
    scrape_page(base_url)

    for page in range(2, 26):
        page_url = f'{base_url}&page={page}&affinityOverride=default'
        scrape_page(page_url)
        time.sleep(2)  # Añadir una pausa entre las solicitudes para no sobrecargar el servidor

    # Cerrar la conexión a la base de datos
    cursor.close()
    db.close()
    print("Conexión cerrada")
except (Exception, psycopg2.Error) as error:
    print("Error al conectar a la base de datos", error)
