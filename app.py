import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.font_manager as font_manager
import seaborn as sns
import sys

font_legend = font_manager.FontProperties(family='Arial', style='normal', size=10)

def encode_depto_pretty(series):
    "Codifica departamento INE, formateado"
    deptos_dict = {
        'Montevideo': 1,
        'Artigas': 2,
        'Canelones': 3,
        'Cerro Largo': 4,
        'Colonia': 5,
        'Durazno': 6,
        'Flores': 7,
        'Florida': 8,
        'Lavalleja': 9,
        'Maldonado': 10,
        'Paysandú': 11,
        'Río Negro': 12,
        'Rivera': 13,
        'Rocha': 14,
        'Salto': 15,
        'San José': 16,
        'Soriano': 17,
        'Tacuarembó': 18,
        'Treinta y Tres': 19
        }
    cod = series.map(deptos_dict).values

    return cod[0]


#icon = 'data/flag.png'

#st.set_page_config(page_title='Test', page_icon = icon)
st.set_page_config(page_title='Migrantes internos en Uruguay')

st.title("Migrantes internos en Uruguay 🇺🇾")

desc = """
Aplicación para comparar datos
demográficos de los migrantes internos en Uruguay,
según los datos del Censo INE 2011.

*Desarrollada por Guillermo D'Angelo.*
"""

st.caption(desc)

@st.cache(persist=True)
def load_data_pickle(data_path):
    data = pd.read_pickle(data_path, compression='gzip')
    return data

files = [
    'data/deptos.csv',
    'data/datos_tablero.csv',
    'data/coords.csv',
    ]

deptos, data_group , coords = [pd.read_csv(i) for i in files]

dd = pd.read_csv('data/dd_deptos.csv', sep=';')

nom_depto = [
    'Montevideo', 'Artigas', 'Canelones',
    'Cerro Largo', 'Colonia', 'Durazno',
    'Flores', 'Florida', 'Lavalleja',
    'Maldonado', 'Paysandú', 'Río Negro',
    'Rivera', 'Rocha', 'Salto', 'San José',
    'Soriano', 'Tacuarembó', 'Treinta y Tres'
    ]

agrup_mig = load_data_pickle('data/agrup_piramides_tablero.pkl')


#### sidebars #####
st.sidebar.title('Selección de departamentos')

side_text = """
Seleccione un departamento de residencia en 2006 y uno de residencia habitual en 2011,
a partir de dicha selección se presentarán los datos
"""

st.sidebar.markdown(side_text)

# sidebar 1
nom_depto1 = st.sidebar.selectbox("Departamento de residencia en 2006", nom_depto, key=1, index=3)
depto1 = encode_depto_pretty(pd.Series(nom_depto1))

# sidebar 2
nom_depto2 = st.sidebar.selectbox("Departamento de residencia habitual en 2011", nom_depto, key=3, index=9)
depto2 = encode_depto_pretty(pd.Series(nom_depto2))

if depto1 == depto2:
    st.markdown('**Error: los departamentos de residencia en 2006 y de residencia habitual en 2011 deben ser diferentes**')

# extrae datos en objetos
d1 = data_group.depto_origen==depto1
d2 = data_group.depto_destino==depto2
data = data_group.loc[(d1) & (d2)]

# crea código de díada
cod = int(data.cod.values)

# filtra datos diádicos
dd_filtrado = dd.loc[dd.cod==cod]



# header
subhead = f'Migrantes desde **{nom_depto1}** a **{nom_depto2}**'
st.subheader(subhead)

# Métricas
pob =   str(data.n.values[0])
imasc_int = round(data.ind_masc.values[0])
imasc = str(imasc_int)
emed =  str(data.edad_mediana.values[0])
dist =  str(dd_filtrado.dist_km.values[0])

delta_imasc = str(95 - imasc_int)

n_migrantes = 148759

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nro. migrantes", pob)
col2.metric("Índice masculinidad", imasc, delta_imasc, delta_color='off')
col3.metric("Edad mediana", emed + ' años')
col4.metric('Distancia por rutas', dist + ' km')


# textos
text = """Los migrantes internos con residencia en **{}** en 2006 y residencia habitual en **{}** en 2011 fueron **{}**, según datos censales.

El índice de masculinidad de dicha población fue **{}** hombres por cada 100 mujeres.

La edad mediana era de **{} años**, en tanto la del total de la población era de 34 años,
la del total de la población migrante interna era de 28 años.

La distancia por rutas entre los centros medios de población de ambos
departamentos es **{}** km.
"""

data_text = text.format(nom_depto1, nom_depto2, pob, imasc, emed, dist)


with st.expander("Ver más"):
     st.markdown(data_text)




# mapita de folium
center = [-32.706, -56.0284]

m = folium.Map(
    location=center,
    zoom_start=6,
    tiles='Cartodb Positron',
    width='100%',
    height='100%',
    left='0%',
    top='0%'
    )

col_c = ['lat', 'lon']
coords_1 = list(coords.loc[coords.DEPTO==depto1, col_c].values[0])
coords_2 = list(coords.loc[coords.DEPTO==depto2, col_c].values[0])

# add marker
ic1 = folium.Icon(color="darkblue",  icon="bullseye", prefix='fa')
ic2 = folium.Icon(color="cadetblue", icon="bullseye", prefix='fa')
folium.Marker(coords_1, popup=nom_depto1, icon=ic1).add_to(m)
folium.Marker(coords_2, popup=nom_depto2, icon=ic2).add_to(m)

loc = [coords_1, coords_2]
line = folium.PolyLine(locations=loc, color='gray', weight=4)

m.add_child(line)

m.fit_bounds([coords_1, coords_2], max_zoom=9) 

# call to render Folium map in Streamlit
folium_static(m)


# pirámides de población
data_pir = agrup_mig.loc[agrup_mig.cod == cod]

# función para graficar
def bars_pyramid(df, axis, col_agrup, colors, bar_order):
    "Grafica barras para pirámdes"
    for c, group in zip(colors, df[col_agrup].unique()):
        sns.barplot(x='porc_pers',
                    y='tramo',
                    data=df.loc[df[col_agrup]==group, :],
                    order = bar_order,
                    color=c,
                    ax=axis)

def etiquetar_sexos(x_position, y_position, ax_name, colors, font_size):
        # Varones
        ax_name.text(x_position*-1, y_position, 'Varones',
        horizontalalignment='left',
        color=colors[0], fontsize=font_size)
        # Mujeres
        ax_name.text(x_position, y_position, 'Mujeres',
        horizontalalignment='right',
        color=colors[1], fontsize=font_size)

# vector de etiquetas para cada tramo
y_labels = ['+95','90-94','85-89','80-84','75-79','70-74',
            '65-69','60-64','55-59','50-54','45-49','40-44',
            '35-39','30-34','25-29','20-24','15-19','10-14',
            '5-9','0-4']


fig, ax  = plt.subplots(1, figsize= ( 10, 6 ))

# plot
group_col = 'sexo_label'
order_of_bars = y_labels
colors = ['#7b3294', '#008837']
label=['sexo', '']

bars_pyramid(data_pir, ax, 'sexo_label', colors, y_labels)

tit = f'Pirámide de población de migrantes entre {nom_depto1} y {nom_depto2}'
ax.set_title(tit, pad=20)

ax.set_axisbelow(True)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.axvline(linewidth=1, color='black')
ax.set_xlim([-9,9])
ax.set_xticklabels(['10%','8%','6%','4%','2%','0','2%','4%','6%','8%'])

_ = [s.set_visible(False) for s in ax.spines.values()]
_ = [t.set_visible(False) for t in ax.get_yticklines()]

etiquetar_sexos(3, 0, ax, colors, 10)

    
st.pyplot(fig)




st.dataframe(dd.head())
