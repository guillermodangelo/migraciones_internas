import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import seaborn as sns

#icon = 'data/flag.png'

#st.set_page_config(page_title='Test', page_icon = icon)
st.set_page_config(page_title='Test')

st.title("Test")
st.markdown("Aplicación para comparar pirámides de población de dos localidades "
            "de Uruguay según datos del Censo INE 2011. "
            "*Desarrollada por Guillermo D'Angelo.*")

@st.cache(persist=True)
def load_data(data_path):
    data = pd.read_csv(data_path)
    return data

deptos = load_data('data/deptos.csv')
data_group = load_data('data/datos_tablero.csv')
coords = load_data('data/coords.csv')


#### sidebars #####
st.sidebar.title('Selección de departamentos 👇')

nom_depto = list(deptos.DEPTO)

# sidebar 1
nom_depto1 = st.sidebar.selectbox("Departamento", nom_depto, key=1, index=3)
depto1 = list(deptos.loc[deptos.DEPTO == nom_depto1, 'COD'])[0]

# sidebar 2
nom_depto2 = st.sidebar.selectbox("Departamento", nom_depto, key=3, index=9)
depto2 = list(deptos.loc[deptos.DEPTO == nom_depto2, 'COD'])[0]

# extrae datos en objetos
d1 = data_group.depto_origen==depto1
d2 = data_group.depto_destino==depto2
data = data_group.loc[(d1) & (d2)]


st.dataframe(data)


# mapita de folium
center = [-32.706, -56.0284]

m = folium.Map(location=center, zoom_start=6, tiles='OpenStreetMap',
               width='70%', height='70%', left='0%', top='0%')

col_c = ['lat', 'lon']
coords_1 = list(coords.loc[coords.DEPTO==depto1, col_c].values[0])
coords_2 = list(coords.loc[coords.DEPTO==depto2, col_c].values[0])


# add marker
folium.Marker(coords_1, popup=nom_depto1).add_to(m)
folium.Marker(coords_2, popup=nom_depto2).add_to(m)

line = folium.PolyLine(locations=[coords_1, coords_2],
color='red', weight=5)

m.add_child(line)

# call to render Folium map in Streamlit
folium_static(m)


# static text
pob = data.n.values[0]
imasc = data.ind_masc.values[0]

# textos
text = """La díada seleccionada consta de **{}** personas migrantes
internas con un índice de masculinidad de **{}** hombres
por cada 100 mujeres."""

data_text = text.format(pob, imasc)

st.markdown(data_text)



# def calc_props(df):
#     df['porc_pers'] = (df.personas / df.personas.sum())*100
#     df['personas'] = np.where(df['sexo'] ==1, -df['personas'], df['personas'])
#     df['porc_pers'] = np.where(df['sexo'] ==1, -df['porc_pers'], df['porc_pers'])
#     return df

# ciudad_1_gr = calc_props(data_tramos.loc[data_tramos.CODLOC == codloc1])
# ciudad_2_gr = calc_props(data_tramos.loc[data_tramos.CODLOC == codloc2])

# # pirmides de poblacin
# fig, (ax1, ax2)  = plt.subplots(1,2, figsize= ( 10, 6 ), sharex= True, sharey='row')

# bins = [0 if i==-1 else i for i in range(-1,95,5)]
# bins.append(120)
# l1 = [str(i) if i==0 else str(i+1) for i in bins][:19]
# l2 = [str(i) for i in bins][1:]
# labels = ['-'.join([l1[i], l2[i]]) for i in range(19)]
# labels.append('+95')
    
# # plot
# group_col = 'sexo_label'
# order_of_bars = labels[::-1]
# colors = ['skyblue', 'seagreen']
# label=['sexo', 'sasa']

# array_sexo = ciudad_1_gr[group_col].unique()

# for c, group in zip(colors, array_sexo):
#     sns.barplot(x='porc_pers', y='tramo_label', data=ciudad_1_gr.loc[ciudad_1_gr[group_col]==group, :],
#                 order = order_of_bars, color=c, label=group, ax=ax1)

# for c, group in zip(colors, array_sexo):
#     sns.barplot(x='porc_pers', y='tramo_label', data=ciudad_2_gr.loc[ciudad_2_gr[group_col]==group, :],
#                 order = order_of_bars, color=c, label=group, ax=ax2)

# ax1.set_title(nom_loc1, pad=20)
# ax2.set_title(nom_loc2, pad=20)

# labels = ['8%', '6%','4%','2%','0','2%','4%','6%']

# for i in [ax1, ax2]:
#     i.set_axisbelow(True)
#     i.set_ylabel(None)
#     i.set_xlabel(None)
#     i.set_xlim([-7.5, 7.5])
#     i.axvline(linewidth=1, color='black')
#     i.set_xticklabels(labels)
#     _ =[s.set_visible(False) for s in i.spines.values()]
#     _ =[t.set_visible(False) for t in i.get_yticklines()]

# ax1.text(-3, 0.5, 'Varones',
#         horizontalalignment='left',
#         color='cadetblue', fontsize=10)

# ax1.text(3, 0.5, 'Mujeres',
#         horizontalalignment='right',
#         color='green', fontsize=10)

# st.pyplot(fig)

