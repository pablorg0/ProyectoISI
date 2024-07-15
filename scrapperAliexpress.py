import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
import config  # Archivo config.py que contiene db_config con la configuración de la base de datos

# Conectar a la base de datos MySQL
db = mysql.connector.connect(**config.db_config)
cursor = db.cursor()

# Crear la tabla si no existe
cursor.execute("DROP TABLE IF EXISTS resistant_smartphones;")
cursor.execute("""
    CREATE TABLE resistant_smartphones (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2),
        url VARCHAR(255),
        img_url VARCHAR(255)
    );
""")

# Función para scrapeear una página
def scrape_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Unable to fetch page {url}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = soup.find_all('div', class_='JIIxO')
    for product in products:
        name_tag = product.find('a', class_='_3t7zg _2f4Ho')
        if not name_tag:
            continue

        name = name_tag.text.strip()
        link = 'https:' + name_tag['href']
        
        price_tag = product.find('div', class_='mGXnE _37W_B')
        if price_tag:
            price_text = price_tag.text.strip().replace('€', '').replace(',', '.')
            price_match = re.search(r'\d+(\.\d+)?', price_text)
            if price_match:
                price = float(price_match.group())
            else:
                price = None
        else:
            price = None

        img_tag = product.find('img', class_='JMIpe _2vWXo')
        img_url = 'https:' + img_tag['src'] if img_tag else None
        
        # Insertar en la base de datos
        cursor.execute("""
            INSERT INTO resistant_smartphones (name, price, url, img_url)
            VALUES (%s, %s, %s, %s)
        """, (name, price, link, img_url))

    db.commit()

# Scrapeando las páginas permitidas
base_url = 'https://es.aliexpress.com/w/wholesale-Tel%C3%A9fonos-inteligentes-resistentes.html?isFromCategory=y&categoryUrlParams=%7B%22q%22%3A%22Tel%C3%A9fonos+inteligentes+resistentes%22%2C%22s%22%3A%22qp_nw%22%2C%22osf%22%3A%22categoryNagivateOld%22%2C%22sg_search_params%22%3A%22%22%2C%22guide_trace%22%3A%22dd2a3b13-ec9a-4b14-9347-c4110f190efc%22%2C%22scene_id%22%3A%2230630%22%2C%22searchBizScene%22%3A%22openSearch%22%2C%22recog_lang%22%3A%22es%22%2C%22bizScene%22%3A%22categoryNagivateOld%22%2C%22guideModule%22%3A%22unknown%22%2C%22postCatIds%22%3A%22509%22%2C%22scene%22%3A%22category_navigate%22%7D&g=y&SearchText=Tel%C3%A9fonos+inteligentes+resistentes&_pgn={}'
for page in range(2, 11):  # De la página 1 a la 10
    url = base_url.format(page)
    scrape_page(url)

# Cerrar la conexión a la base de datos
cursor.close()
db.close()

