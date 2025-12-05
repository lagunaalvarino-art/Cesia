import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

## TAMAÑO DEL DATAFRAME
variables = df_cont.shape[0]
registros = df_cont.shape[1]
num_deptos = df_cont['DEPARTAMENTO'].nunique()
num_mpios = df_cont['MUNICIPIO'].nunique()

## ORDENAR EL DATAFRAME POR AÑO Y DEPARTAMENTO DE MAYOR A MENOR
df_depto_anio = df_cont.groupby(['DEPARTAMENTO', 'AÑO SERVICIO'])['ENERGÍA ACTIVA'].sum().reset_index()

## GENERAR EL LISTADO DE DEPARTAMENTOS
lista_deptos = df_depto_anio['DEPARTAMENTO'].unique().tolist()

################################################
################# VISUALIZACIÓN ################
################################################

##############  CONFIGURACIÓN DE LA PÁGINA  ##############
st.set_page_config(
    page_title='Análisis de la Energía en Colombia',
    page_icon='⚡',
    layout='centered'
)

st.markdown(
    '''
    <style>
        .block-container {
            max-width: 1200px;
        }
    ''',unsafe_allow_html=True
)


st.image('./img/encabezado.png', use_container_width=True)


##############  DETALLES DEL DATASET  ##############

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
        st.metric('Municipios', num_mpios, border=True)

    if st.checkbox('Mostrar detalles de la fuente de los datos'):
        st.write('Conjunto de datos obtenidos del portal de datos abiertos del Gobierno Nacional de Colombia.')
        st.write('Disponible en: https://www.datos.gov.co/Minas-y-Energ-a/Estado-de-la-prestaci-n-del-servicio-de-energ-a-en/3ebi-d83g')

    with st.expander('Ver conjunto de Datos completo'):
        st.dataframe(df_cont)


##############  GRAFICO INTERACTIVO DE BARRAS POR DEPARTAMENTO Y AÑO  ##############

with st.container(border=True):
    st.subheader('Evolución de la Energía Activa por Departamento')

    depto_seleccionado = st.selectbox(
        'Seleccione un Departamento:',
        options=lista_deptos
    )

    condicion_filtro = df_depto_anio['DEPARTAMENTO'] == depto_seleccionado
    df_departamento = df_depto_anio[condicion_filtro]

    ## Crear el gráfico de barras
    # 1. Crear el objeto Figure
    fig_barras = go.Figure()

    # 2. Agregar las barras a fig_barras
    fig_barras.add_trace(go.Bar(
        x=df_departamento['ENERGÍA ACTIVA'],
        y=df_departamento['AÑO SERVICIO'].astype(str),
        orientation='h',
        text=df_departamento['ENERGÍA ACTIVA'],
        marker_color="#3785ba",
        textposition='auto'
    ))

    # 3. Actualizar el diseño del gráfico
    fig_barras.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'category ascending'}
    )

    # 4. Mostrar el gráfico
    st.plotly_chart(fig_barras, use_container_width=True)
    

