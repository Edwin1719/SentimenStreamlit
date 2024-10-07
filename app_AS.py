import streamlit as st
import pandas as pd
from transformers import pipeline
from io import BytesIO
from st_social_media_links import SocialMediaIcons

# Configurar el pipeline de análisis de sentimientos
nlp = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Función para realizar análisis de sentimientos y categorizarlos
def analizar_y_traducir(comentario):
    resultado = nlp(comentario)[0]['label']
    return 'Negativo' if resultado in ['1 star', '2 stars'] else 'Neutro' if resultado == '3 stars' else 'Positivo'

# Título de la aplicación
st.title("Análisis de Sentimientos")

# Cargar archivo
archivo = st.file_uploader("Cargar archivo CSV o Excel", type=["csv", "xlsx"])

if archivo is not None:
    # Leer archivo según el tipo
    if archivo.name.endswith('.csv'):
        df = pd.read_csv(archivo, delimiter=';')
    else:
        df = pd.read_excel(archivo)

    # Verificar que la columna 'Comentario' existe
    if 'Comentario' in df.columns:
        # Aplicar la función de análisis de sentimientos
        df['Sentimiento_Categorizado'] = df['Comentario'].apply(analizar_y_traducir)

        # Mostrar los resultados
        st.write("Resultados del análisis de sentimientos:")
        st.dataframe(df[['Comentario', 'Sentimiento_Categorizado']])

        # Crear un buffer de BytesIO para guardar el archivo Excel
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        # Descargar el archivo con los resultados
        st.download_button(
            label="Descargar resultados",
            data=buffer.getvalue(),
            file_name='Analisis_Sentimientos.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.error("El archivo no contiene una columna llamada 'Comentario'.")

# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()