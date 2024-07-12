import mysql.connector

config = {
  'host': 'rafadgvc.mysql.database.azure.com',
    'user': 'rafadgvc',
    'password': 'FitSuppFinder1',
    'database': 'FitSuppFinder'
}

# Inicia la conexión
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#Para productsWalmart
queryWalmart = "SELECT * FROM unlocked_phones"
cursor.execute(queryWalmart)

with open('productsWalmart.txt', 'w') as f:
    for (id, name, price, url, img_url) in cursor:
        f.write(f'{id} \\ {name} \\ {price} \\ {url} \\ {img_url}\n')

#Para productsAliexpress
queryAliexpress = "SELECT * FROM resistant_smartphones"
cursor.execute(queryAliexpress)

with open('productsAliexpress.txt', 'w') as f:
    for (id, name, price, url, img_url) in cursor:
        f.write(f'{id} \\ {name} \\ {price} \\ {url} \\ {img_url}\n')

#Para FakeStoreAPI
queryAmazon = "SELECT * FROM electronics"
cursor.execute(queryAmazon)

with open('productsAPI.txt', 'w') as f:
    for (id, name, brand, price, quantity, measure, url) in cursor:
        f.write(f'{id} \\ {name} \\ {brand} \\ {price} \\ {quantity} \\ {measure} \\ {url}\n')

cursor.close()
cnx.close()
