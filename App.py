import streamlit as st
import pandas as pd


################################################
###### CARGA, PREPROCESAMIENTO Y ANÁLISIS ######
################################################

### CARGA DE LOS DATOS
url = './data/zni.csv'
df_original = pd.read_csv(url)

### FILTRAR EL DATASET POR ALGUNAS COLUMNAS
df = df_original[['AÑO SERVICIO','DEPARTAMENTO', 'MUNICIPIO', 'ENERGÍA ACTIVA', 'ENERGÍA REACTIVA', 'POTENCIA MÁXIMA']]

df['ENERGÍA ACTIVA'] = df['ENERGÍA ACTIVA'].str.replace(',','').astype(float).astype(int)
df['ENERGÍA REACTIVA'] = df['ENERGÍA REACTIVA'].str.replace(',','').astype(float).astype(int)
df['POTENCIA MÁXIMA'] = df['POTENCIA MÁXIMA'].str.replace(',','').astype(float).astype(int)

lst_cambio = [['Á','A'], ['É','E'], ['Í','I'], ['Ó','O'], ['Ú','U']]

for viejo, nuevo in lst_cambio:
    df['DEPARTAMENTO'] = df['DEPARTAMENTO'].str.replace(viejo,nuevo)
    df['MUNICIPIO'] = df['MUNICIPIO'].str.replace(viejo,nuevo)

### LISTA DE VALORES DE LA CONDICION PARA IDENTIFICAR
### LA ZONA NO CONTINENTAL
condicion = [
    'ARCHIPIELAGO DE SAN ANDRES',
    'ARCHIPIELAGO DE SAN ANDRES y PROVIDENCIA',
    'ARCHIPIELAGO DE SAN ANDRES, PROVIDENCIA Y SANTA CATALINA'
]

### FILTRAR con las filas que NO cumplan la Condición
### de que DEPARTAMENTO esté en la lista
df_cont = df[~df['DEPARTAMENTO'].isin(condicion)]

variables = df_cont.shape[0]
registros = df_cont.shape[1]
num_deptos = df_cont['DEPARTAMENTO'].nunique()
num_mpios = df_cont['MUNICIPIO'].nunique()


st.image('./img/Imag.png')
st.dataframe(df_cont)

with st.container(border=True):
    st.subheader('Descripción del Dataset')
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Variables', variables, border=True)

    with col2:
        st.metric('Registros', registros, border=True)

    with col3:
        st.metric('Departamentos', num_deptos, border=True)

    with col4:
        st.metric('Municipios',num_mpios, border=True)

if st.checkbox('Mostrar detalle de la fuente de los datos'):
    st.write('Conjunto de datos obtenidos del portal de datos abiertos de colombia')
    st.write('Disponible en https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g/about_data')
with st.expander('Ver conjuto de datos completo'):
    st.dataframe(df_cont)