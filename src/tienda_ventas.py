import pandas as pd
import streamlit as st
import graficos as graf

st.set_page_config(layout= 'wide')

# CSS css
with open('src/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#load_css('style.css')
# columnas top contienen total revenue y el total de ventas.
top_col1, top_col2, top_col3 = st.columns(3)
with top_col1:
    st.caption('Total Revenue')
    placeholder = st.empty() # espacio reselvado
with top_col2:
    st.caption('')
with top_col3:
    st.caption('Total Product Sales')
    placeholder2 = st.empty() # espacio reselvado
    
    
# funcion para agragar columna de temporadas al df
def temporada(mes):
    if mes in [12,1,2]:
        return 'Winter'
    elif mes in [3,4,5]:
        return 'Spring'
    elif mes in [6,7,8]:
        return 'Summer'
    elif mes in [9,10,11]:
        return 'Fall'
    

st.title('Sales and Performance Analysis 📈')


st.sidebar.image('src/Python_PNG.png')


# habrir df y darle formato a la columna de tiempo
df_final = pd.read_csv('src/df_final.csv', sep=',')
df_final['fecha_compra'] = pd.to_datetime(df_final['fecha_compra'], errors='coerce')
df_final['año_compra'] = df_final['año_compra'].astype(str)
# crear columna temporada
df_final['temporada'] = df_final['mes_compra'].apply(temporada)



# filtro para las CIUDADES
estados = sorted(list(df_final['ciudad_nombre'].unique()))
estado = st.sidebar.multiselect("Estates", estados)

if estado: 
    df_final = df_final[df_final['ciudad_nombre'].isin(estado)]

# filtro para el tipo de PRODUCTO
productos = sorted(list(df_final['tipo_producto'].unique()))
productos.insert(0,'All Products')
producto = st.sidebar.selectbox('Select Produc', productos)

if producto != 'All Products':
    df_final = df_final[df_final['tipo_producto'] == producto]


# filtro para los AÑOS
años = sorted(list(df_final['año_compra'].unique()))
año = st.sidebar.multiselect('Years', años)

if año:
    df_final = df_final[df_final['año_compra'].isin(año)]
  
  
# filtro para las temporadas
temporadas = sorted(list(df_final['temporada'].unique()))
temporadas.insert(0,'All Seasons')
temporada = st.sidebar.selectbox('Select Season', temporadas)

if temporada != 'All Seasons':
    df_final = df_final[df_final['temporada'] == temporada]
      

# LLAMAR LOS GRAFICOS
grafico_linea = graf.pregunta_2(df_final)
grafico_barra = graf.pregunta_3(df_final)
grafico_mapa = graf.pregunta_4(df_final)
grafico_pizza = graf.pregunta_1(df_final)
grafico_d = graf.grafico_d(df_final)


# CREANDO 2 COLUMNAS y mastral grafici dentro de las columnas 
col1, col2 = st.columns([2, 1])
with col1:
    #st.plotly_chart(grafico_d, use_container_width=True)
    st.plotly_chart(grafico_mapa, use_container_width=True)
with col2:
    st.plotly_chart(grafico_pizza, use_container_width=True)
    

#MOSTRAL LOS GRAFICOS inferiores que no estan dentro de las columnas.
st.plotly_chart(grafico_linea, use_container_width=True)
st.plotly_chart(grafico_barra, use_container_width=True)


total_ingresos = df_final['ingresos_netos'].sum()
total_ventas = df_final['cantidad'].sum()

def formatear_numero(numero):
    if numero >= 1_000_000:
        return f"{numero/1_000_000:.2f}M"
    elif numero >= 1_000:
        return f"{numero / 1_000:.2f}K"
    else:
        return str(numero)
total_ingresos_f = formatear_numero(total_ingresos)
total_ventas_f = formatear_numero(total_ventas)
placeholder.markdown(f'<div class="custon-container">${total_ingresos_f}</div>', unsafe_allow_html=True)
placeholder2.markdown(f'<div class="custon-container">{total_ventas_f}</div>', unsafe_allow_html=True)
