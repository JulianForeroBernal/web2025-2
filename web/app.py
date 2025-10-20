from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import os

app = Flask(__name__)

def cargar_noticias_xml():
    """
    Función para cargar y parsear el archivo XML de noticias
    """
    try:
        # Ruta del archivo XML - buscar en diferentes ubicaciones
        posibles_rutas = [
            os.path.join(os.path.dirname(__file__), '..', 'notiTegnoAp.xml'),
            r'c:\Python\20251014\notiTegnoAp.xml',
            'notiTegnoAp.xml'
        ]
        
        xml_path = None
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                xml_path = ruta
                break
        
        if xml_path is None:
            return "Error: Archivo notiTegnoAp.xml no encontrado"
        
        # Parsear el XML
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        # Extraer información del canal
        channel = root.find('channel')
        if channel is None:
            return "Error: No se encontró el elemento 'channel' en el XML"
        
        noticias = []
        
        # Extraer cada noticia (item)
        for i, item in enumerate(channel.findall('item'), 1):
            # Obtener imagen de enclosure
            enclosure = item.find('enclosure')
            imagen_url = ''
            if enclosure is not None and enclosure.get('url'):
                imagen_url = enclosure.get('url')
            
            noticia = {
                'id': i,
                'titulo': item.find('title').text if item.find('title') is not None else 'Sin título',
                'descripcion': item.find('description').text if item.find('description') is not None else 'Sin descripción',
                'enlace': item.find('link').text if item.find('link') is not None else '#',
                'fecha': item.find('pubDate').text if item.find('pubDate') is not None else 'Sin fecha',
                'categoria': item.find('category').text if item.find('category') is not None else 'Sin categoría',
                'imagen': imagen_url
            }
            noticias.append(noticia)
        
        return noticias
    except Exception as e:
        return f"Error al cargar XML: {str(e)}"

@app.route('/')
def index():
    """Ruta principal que muestra las noticias"""
    noticias = cargar_noticias_xml()
    return render_template('noticia.html', noticias=noticias)

@app.route('/api/noticias')
def api_noticias():
    """API endpoint para obtener noticias en formato JSON"""
    noticias = cargar_noticias_xml()
    return jsonify(noticias)

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    """Ruta del formulario original"""
    resultado = None
    if request.method == 'POST':
        try:
            # Aquí puedes agregar la lógica del formulario
            resultado = "Formulario procesado correctamente"
        except (ValueError, TypeError):
            resultado = "Error: Entrada no válida"
    return render_template('formulario.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)