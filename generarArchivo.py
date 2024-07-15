import mysql.connector

config = {
    'host': 'proyectoisiv2-server.postgres.database.azure.com',
    'user': 'uimpsotsiy',
    'password': '8uoyerOVvg9$x2Ru',
    'database': 'proyectoisiv2-database'
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
queryAPI = "SELECT * FROM electronics"
cursor.execute(queryAPI)

with open('productsAPI.txt', 'w') as f:
    for (id, name, brand, price, quantity, measure, url) in cursor:
        f.write(f'{id} \\ {name} \\ {brand} \\ {price} \\ {quantity} \\ {measure} \\ {url}\n')

cursor.close()
cnx.close()
