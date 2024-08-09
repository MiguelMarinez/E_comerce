import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import json
import requests


def pregunta_1(df):
    
    
    top_productos = df.groupby('tipo_producto')['cantidad'].sum().sort_values(ascending=False).head(5)
    top_productos = top_productos.reset_index()
    
  
    
    fig_pizza = px.pie(top_productos, 
                   values='cantidad', 
                   names='tipo_producto', 
                   title='Top 5 Best-Selling Products',
                   color='tipo_producto',
                   color_discrete_sequence=px.colors.sequential.Blues_r  # Usa una escala de azules
                   )

    fig_pizza.update_layout(
        title={'text':'Top 5 Best-Selling Products',
               'y':0.90, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top', 'font':{'size':15}},
       
        template='plotly_dark',
        font=dict(
            family='Arial, sans-serif',
            size=10,
            color='white'
        ),
        showlegend=False,
        margin=dict(l=10, r=10, t=100, b=10)
    )

    fig_pizza.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(color='white'))
    
    fig_pizza.update_traces(hovertemplate="<br><span style='color: #ffffff;'>Quantity: %{value:,.0f}<extra></extra>")
    
    return fig_pizza




def pregunta_2(df):
    
    
    
    df['ingresos_netos'] = df['valor_total'] - df['costo_envio']
    ingresos_historico = df.groupby(['año_compra', 'mes_compra'])['ingresos_netos'].sum().reset_index()
    
    #ingresos_historico.head()
    
    # para mapear números de mes a nombres de mes
    month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'Jun', 
               7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}


    fig = px.line(ingresos_historico, x='mes_compra', y='ingresos_netos', color='año_compra', markers=True,
                labels={'ingresos_netos': 'Ingresos Netos', 'mes_compra': 'Mes', 'año_compra': 'Año'},
                title='Historical Evolution of Net Revenue by Year',
                hover_data={'ingresos_netos': ':.2f'})

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Net Revenue',
        legend_title_text='Year',
        template='plotly_dark', 
        xaxis=dict(
            tickmode='array',
            tickvals=list(month_names.keys()),
            ticktext=list(month_names.values()),
            tickangle=45
        )
    )

    #fig.update_traces(line=dict(color='blue'), )
    #fig.update_traces(line=dict(color='red'), selector=dict(name='2020'))
    #fig.update_traces(line=dict(color='green'),selector=dict(name='2021'))

    color_map = {2019: 'blue', 2020: 'red', 2021: 'green'}
    for year, color in color_map.items():
        fig.update_traces(
            line=dict(color=color),
            selector=dict(name=str(year)),
            hovertemplate=f'Year: {year}<br>Month: %{{x}}<br>Net Revenue: %{{y:$,.2f}}<extra></extra>')


    return fig




def pregunta_3(df):
    
    
    ingresos_por_vendedor  = df.groupby(['nombre_vendedor','año_compra'])['ingresos_netos'].sum().reset_index()
    ingresos_por_vendedor = ingresos_por_vendedor[ingresos_por_vendedor['nombre_vendedor']!= 'Unknown']
    ingresos_por_vendedor = ingresos_por_vendedor.sort_values(by=['año_compra', 'nombre_vendedor'])
  
    
    
    # Crear la figura
    fig = go.Figure()

    # Agregar las barras apiladas para cada año
    for year in ingresos_por_vendedor['año_compra'].unique():
        df_year = ingresos_por_vendedor[ingresos_por_vendedor['año_compra'] == year]
        fig.add_trace(go.Bar(
            x=df_year['nombre_vendedor'],
            y=df_year['ingresos_netos'],
            name=str(year)
        ))

    # Configurar el diseño del gráfico
    fig.update_layout(
        barmode='group',
        title='Net Revenue by Seller per Year',
        xaxis=dict(title='Seller'),
        yaxis=dict(title='Net Revenue'),
        legend=dict(title='Year'),
        template='plotly_dark',
    )

    fig.update_traces(hovertemplate="<br><span style='color: #ffffff;'>Quantity: $%{value:,.0f}<extra></extra>")

    return fig





def pregunta_4(df):
    
    
    
    # df_final.head(1)
    
    ingresos_por_ciudad = df.groupby('ciudad_nombre')['ingresos_netos'].sum().reset_index()
    ingresos_por_ciudad = ingresos_por_ciudad.sort_values(by='ingresos_netos', ascending=False)
    
    
    # ingresos_por_ciudad.head(5)
    
    # Descargar el archivo GeoJSON de Brasil
    url = 'https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson'
    response = requests.get(url)
    brasil_geojson = response.json()
    
    
    
    
        # Crear el mapa base con las coordenadas de Brasil y las ciudades
    fig = px.choropleth_mapbox(ingresos_por_ciudad,
                            geojson=brasil_geojson,
                            locations='ciudad_nombre',
                            featureidkey="properties.name",
                            color='ingresos_netos',
                            color_continuous_scale='Blues',
                            hover_name='ciudad_nombre',
                            custom_data=['ciudad_nombre','ingresos_netos' ],
                            center={"lat": -14.2350, "lon": -51.9253},
                            mapbox_style="carto-positron",
                            zoom=2.5,
                            title='Revenue by State in Brazil')



    fig.update_layout(#width=600, height=500,
        paper_bgcolor='rgb(18, 22, 29)', 
        plot_bgcolor='rgb(18, 22, 29)',
        title_x=0.12,
        margin={'r':0,'t':70,'l':5,'b':0},
        mapbox=dict(center=dict(lat=-14.2350, lon=-51.9253),
                layers=[
            
                {
                    "source": brasil_geojson,
                    "type": "fill",
                    "below": "traces",
                    "color": "rgba(18, 22, 29)"  # Hacer el área de Brasil transparente
                },
                {
                    "source": {
                        "type": "FeatureCollection",
                        "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[[-180, -90], [180, -90], [180, 90], [-180, 90], [-180, -90]]]
                            }
                        }
                    ]
                    },
                        "type": "fill",
                        "below": "traces",
                        "color": "rgb(18, 22, 29)"  # Fondo negro para áreas fuera de Brasil
                }
                    ]
                
    ),
    
    
    
        coloraxis_colorbar=dict(
        title='Revenue($)',),
        font=dict(
            family="Arial",  
            size=12, 
            color="white")  
    )  
    
    


    fig.update_traces(hovertemplate="<b>City: %{customdata[0]}</b><br>Total Revenue : $%{customdata[1]:,.2f}<extra></extra>", 
                  marker_line_width=0)

    return fig



def grafico_d(df):
    
    
    total_ingesos = df['ingresos_netos'].sum()
    df_ingresos = pd.DataFrame({'labels': ['total_ingesos'], 'ingresos_netos': [total_ingesos]})
    
    fig = px.pie(df_ingresos, values='ingresos_netos', names='labels',hole=0.5)
    
    fig.update_traces(textinfo='none', marker=dict(colors=['green']))
    fig.update_layout(showlegend=False,
                      annotations=[dict(text=f"{total_ingesos:,}", x=0.5, y=0.5, font_size=20, showarrow=False)])
    
    return fig
    
    


    
    
    