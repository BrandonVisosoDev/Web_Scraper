import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def download_image(url, folder_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Extrae el nombre del archivo de la URL
        parsed_url = urlparse(url)
        filename = os.path.join(folder_path, os.path.basename(parsed_url.path))
        
        # Guarda la imagen en la carpeta especificada
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        return filename
    else:
        return None

def scrape_data_with_images(url, image_tag):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encuentra los elementos que contienen los títulos de las noticias
    news_elements = soup.find_all('h5', class_='product-name')  # Ajusta según la estructura del sitio
    
    # Encuentra los elementos que contienen los precios
    price_elements = soup.find_all('span', class_='price product-price')  # Ajusta según la estructura del sitio
    
    # Encuentra los elementos que contienen las imágenes
    image_elements = soup.find_all(image_tag)  # Ajusta según la etiqueta de las imágenes
    
    # Crea la carpeta para las imágenes si no existe
    image_folder = "images"
    os.makedirs(image_folder, exist_ok=True)
    
    # Extrae los títulos de las noticias, los precios y descarga las imágenes
    news_data = []
    for i, element in enumerate(news_elements):
        title = element.text.strip()
        price = price_elements[i].text.strip() if i < len(price_elements) else "Precio no disponible"
        
        # Descarga la imagen y obtén la ruta del archivo descargado
        image_url = urljoin(url, image_elements[i]['src']) if i < len(image_elements) else None
        image_path = download_image(image_url, image_folder) if image_url else None
        
        news_data.append({"title": title, "price": price, "image_path": image_path})
    
    return news_data

# Interfaz de usuario con Streamlit
st.title("Web Scraper Semi-Automático")

st.image("IMG/img.jpg", width  = 600 )

# Ingresa la URL del sitio web a scrapear
url_input = st.text_input("Ingresa la URL del sitio web:", "https://www.ejemplo.com/productos")

# Ingresa la etiqueta de las imágenes
image_tag_input = st.text_input("Ingresa la etiqueta de las imágenes (por ejemplo, 'img'):", "img")

# Sección para mostrar la información
if st.button("Mostrar Información"):
    if url_input:
        st.info("¡Obteniendo información! Por favor, espera...")
        
        # Llamada a la función de scraping con información
        scraped_data = scrape_data_with_images(url_input, image_tag_input)
        
        st.success("Información obtenida con éxito")
        
        # Muestra los títulos de las noticias y los precios correspondientes
        st.write("Información scrapada:")
        for data in scraped_data:
            st.write(f"- Título: {data['title']}, Precio: {data['price']}")
    else:
        st.warning("Por favor, ingresa una URL válida.")

