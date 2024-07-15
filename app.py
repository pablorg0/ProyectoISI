from flask import Flask, render_template, request, redirect, url_for
import subprocess


app = Flask(__name__)

def run_script(script_name):
    #"""Ejecuta un script de Python."""
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error ejecutando {script_name}: {result.stderr}")
    else:
        print(f"{script_name} ejecutado con éxito")
        

def sort_products(products):
    def sort_key(product):
        ratio = product['price']
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

def read_api(file_name):
    products = []
    if not os.path.exists(file_name):
        return products

    with open(file_name, 'r') as f:
        lines = f.readlines()

        for line in lines:
            columns = line.strip().split('\\')
            product = {
                'id': int(columns[0]),
                'name': columns[1],
                'price': float(columns[2]),
                'description': columns[3],
                'category': columns[4],
                'image': columns[5],
                'url': columns[6]
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
    # Ejecutar scripts de scraping y generación de archivos
    run_script('scrapperAliexpress.py')
    run_script('scrapperWalmart.py')
    
    return render_template('index.html')
    
    run_script('FakeStoreApi.py')
    run_script('generarArchivo.py')

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

    productsAPI = read_api('productsAPI.txt')
    resultsAPI = consulta(productsAPI, query)

    # Combinar los resultados en una lista
    results = resultsAliexpress + resultsWalmart + resultsAPI

    # Ordenar los resultados
    sort_products(results)

    return results

if __name__ == '__main__':
    app.run()
