import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

def crawl(url):
    try:
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa

        # Analizar el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todas las etiquetas <a> y obtener sus enlaces
        links = soup.find_all('a', href=True)

        data = {}

        # Iterar sobre cada enlace encontrado
        for link in links:
            # Obtener el enlace
            link_url = urljoin(url, link['href'])  # Convertir el enlace a una URL absoluta

            # Realizar una solicitud HTTP al enlace
            link_response = requests.get(link_url)

            # Verificar si la solicitud al enlace fue exitosa
            if link_response.status_code == 200:
                # Analizar el contenido HTML del enlace
                link_soup = BeautifulSoup(link_response.content, 'html.parser')

                # Encontrar todas las etiquetas <h1> y <p>
                h1_tags = link_soup.find_all('h1')
                p_tags = link_soup.find_all('p')

                # Almacenar los elementos encontrados en un diccionario
                data[link_url] = {
                    'h1': [tag.text.strip() for tag in h1_tags],
                    'p': [tag.text.strip() for tag in p_tags]
                }

            else:
                # Si la solicitud al enlace falla, almacenar un array vacío
                data[link_url] = {'h1': [], 'p': []}

        # Guardar los datos en un archivo JSON
        with open('output.json', 'w') as f:
            json.dump(data, f, indent=4)

        print("Datos guardados correctamente en output.json")

    except Exception as e:
        print(f"Error al procesar la URL {url}: {e}")

# Ejemplo de uso
crawl('https://agenty.com/?utm_campaign=20485181654&utm_medium=kwd-498947667&utm_source=&utm_term=web%20scraping%20software&gad_source=1&gclid=CjwKCAjwupGyBhBBEiwA0UcqaIHT4UdK1A9isYpK5HdfhefEnktJWGwK5Oj0RxLeWdJ8gO_rsN1MYBoC9CEQAvD_BwE')
