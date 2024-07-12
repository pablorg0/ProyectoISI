from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def sort_products(products):
    def sort_key(product):
        quantity = product['quantity'] 
        ratio = product['price'] / quantity
        return ratio
    
    products.sort(key=sort_key)



def read_file(file_name):
    products = []
    with open(file_name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            columns = line.strip().split('\\')
            product = {
                'id': int(columns[0]),
                'name': columns[1],
                'price': float(columns[2]),
                'url': columns[3],
                'img_url': columns[4]
            }
            products.append(product)

    return products

def consulta(products, query):
    results = []

    for product in products:
        if query.lower() in product['name'].lower():
            results.append(product)

    return results

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    query = request.form.get('query')

    if query:
        results = execute_query(query)
        return render_template('results.html', query=query, results=results)

    return "Ingrese una consulta de búsqueda válida"

def execute_query(query):
    productsAliexpress = read_file('productsAliexpress.txt')
    resultsAliexpress = consulta(productsAliexpress, query)

    productsWalmart = read_file('productsWalmart.txt')
    resultsWalmart = consulta(productsWalmart, query)

    productsAPI = read_file('productsAPI.txt')
    resultsAPI = consulta(productsAPI, query)

    # Combinar los resultados en una lista
    results = resultsAliexpress + resultsWalmart + resultsAPI

    # Ordenar los resultados
    sort_products(results)

    return results

if __name__ == '__main__':
    app.run()