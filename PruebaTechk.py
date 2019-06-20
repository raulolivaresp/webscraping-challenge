#imports 
import requests
from bs4 import BeautifulSoup
import pandas as pd

#Tomar los links de todas los libros dentro de la pagina web
listaUrls = []
index=0

while True:
    index=index+1    
    indexString = str(index)

    htmlPage = requests.get('http://books.toscrape.com/catalogue/page-'+indexString+'.html')
    
    if htmlPage.status_code==404:
        break
    else:
        soup = BeautifulSoup(htmlPage.text, 'html.parser')
        productos = soup.find_all('article', attrs={'class':'product_pod'}) 

        for producto in productos:
            libroUrl = producto.find('a')['href']
            listaUrls.append('http://books.toscrape.com/catalogue/'+libroUrl)
        
#mensaje total de URLs de libros capturados
print('urls capturadas: '+ str(len(listaUrls)))

#Captura de datos libro por libro

basedatos = []

for libro in listaUrls:
    libroPage = requests.get(libro)
    soup = BeautifulSoup(libroPage.text, 'html.parser')

    #bar home - typo de producto - categoria -libro
    bar = soup.find('ul', attrs={'class':'breadcrumb'})
    categoria = bar.contents[5].find('a').text

    #Detalle del producto
    articulo = soup.find('article', attrs={'class':'product_page'})

    cover = 'http://books.toscrape.com'+str(articulo.find('img')['src'])[5:len(articulo.find('img')['src'])]
    titulo = articulo.find('h1').text
    precio = articulo.find('p', attrs={'class':'price_color'}).text
    stock = articulo.find('p', attrs={'class':'instock availability'}).text.lstrip().rstrip()

    #tabla de informacion del producto
    tabla = articulo.find('table', attrs={'class':'table table-striped'})

    upc = tabla.contents[1].find('td').text
    tipoProducto = tabla.contents[3].find('td').text
    precioExc = tabla.contents[5].find('td').text
    precioInc = tabla.contents[7].find('td').text
    tax = tabla.contents[9].find('td').text
    disponibilidad = tabla.contents[11].find('td').text
    review = tabla.contents[13].find('td').text

    basedatos.append((titulo, precio, stock, categoria, cover, upc, tipoProducto, precioExc, precioInc, tax, disponibilidad, review))


#Guardar datos en csv

archivo = pd.DataFrame(basedatos, columns=['Title', 'Price', 'Stock', 'Category', 'Cover', 'UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability', 'Number of reviews'])

archivo.to_csv('pruebaTechk.csv', index = False, encoding='utf-8')

print('fin proceso')