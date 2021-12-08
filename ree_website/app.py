import streamlit as st
import sqlalchemy
import pymysql
import requests
import folium
#Importing our Packages: Analytics
import pandas as pd
import numpy as np

#Viz libaries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd # library for data analysis
from geopy.geocoders import Nominatim

# convert an address into latitude and longitude values
import requests # library to handle requests
import folium # map rendering library
import streamlit as st #creating an app
#from streamlit_folium import folium_static

#Web App Libraries
from streamlit_folium import folium_static

#Group Paris, Marseille, Lyon by arrondissement
def transform_string(string, separator):
    L = string.split(separator)
    return L[0] if L[0] in ['Paris', 'Marseille', 'Lyon'] else L[0]

#Get data from Mysql on Gcloud
df2 = pd.read_csv('../reestimator/data/final_data.csv', dtype={'code_dep':'object'})
url = 'https://raw.githubusercontent.com/gmanchon/streamlit/master/data/departements.json'
response = requests.get(url).json()
df2= df2[~df2['code_dep'].isin(['974','973','972', '971'])]
df_gv = df2[df2['code_dep'].isin(['13','75','69'])]
df2.commune = df2.commune.apply(lambda x: transform_string(x, ' '))

#Progress Bar
latest_iteration = st.empty()
bar = st.progress(0)
import time
for i in range(100):
    #Update the progress bar with each iteration.
    latest_iteration.text(f'Itération {i+1}')
    bar.progress(i + 1)
    time.sleep(0.01)

#Filters
type_bati = st.sidebar.selectbox(
    'Type de batiment',
    ('Maison', 'Appartement')
)

#Slider
df2.Year = df2.Year.astype('int')
values = st.slider(
    'Selectionner les annees desirees',
     2016, 2020, (2016, 2020))
st.write('Valeurs:', values)

param = st.sidebar.selectbox(
    'Metrics',
    ('Prixm2', 'transactions', 'Avg_sqm', 'No_rooms', 'price', 'Surface'))

# Add a selectbox to the sidebar:
selectbox_city = st.sidebar.selectbox(
    'Ville',
    ('Marseille', 'Paris', 'Lyon'))

if st.checkbox('Sans Métropoles Majeures ?'):
    df2= df2[~df2['commune'].isin(['Paris','Marseille','Lyon'])]

#Filter Final Dataframe
df2= df2[df2['type']== type_bati]
df2= df2[df2['Year'].between(values[0],values[1])]

# Create Final Sum Checkbox
if st.checkbox('Somme?'):
    df2 = df2.groupby(['code_dep','type'])[f"{param}"].sum().reset_index(drop=False)

df2 = df2.groupby(['code_dep','type'])[f"{param}"].mean().reset_index(drop=False)

#Filter Departements in the Final DF
df2.code_dep = df2.code_dep.astype('str')
geodf = df2[['code_dep',f'{param}']]

#Center the Map around the Point of Interest
def center(ville):
   address = f'{ville}, FR'
   geolocator = Nominatim(user_agent="id_explorer")
   location = geolocator.geocode(address)
   latitude = location.latitude
   longitude = location.longitude
   return latitude, longitude

# initialize the first map and store it in a m object
m = folium.Map(location=center('Paris'), zoom_start=5)


def threshold(data, param):
        threshold_scale = np.linspace(geodf[param].min(),
                                      geodf[param].max(),
                                      15, dtype=int)
        # change the numpy array to a list
        threshold_scale = threshold_scale.tolist()
        threshold_scale[-1] = threshold_scale[-1]
        return threshold_scale


def show_maps(data, threshold_scale):
            folium.Choropleth(geo_data=response,
                  name="choropleth",
                  data=geodf,
                  columns=["code_dep", f"{param}"],
                  key_on="feature.properties.code",
                  fill_color="YlOrRd",
                  fill_opacity=0.8,
                  line_opacity=.2,
                  legend_name=f"{param} par commune par departement ",
                  nan_fill_color='white').add_to(m)


            folium_static(m)


show_maps(geodf, threshold(geodf, param))

folium.LayerControl().add_to(m)
'''
# Distribution des paramètres clefs sur les villes principales de France
'''

# Format second map dataframe
df_gv= df_gv[df_gv['type']== type_bati]
df_gv= df_gv[df_gv['Year'].between(values[0],values[1])]
df_gv = df_gv.groupby(['code','type'])[f"{param}"].mean().reset_index(drop=False)
df_gv.code = df_gv.code.astype('str')
geodf2 = df_gv[['code',f'{param}']]

import requests
url2 = 'https://raw.githubusercontent.com/Jehadel/reestimator/JulienVis/notebooks/Julien/arrondissements-millesimes0.geojson'
response2 =  requests.get(url2).json()


#Display the second map
m2 = folium.Map(location=center(f'{selectbox_city}'), zoom_start=11)
def show_maps2(data, threshold_scale):
            folium.Choropleth(geo_data=response2,
                  name="choropleth",
                  data=geodf2,
                  columns=["code", f"{param}"],
                  key_on="feature.properties.code_insee",
                  fill_color="YlOrRd",
                  fill_opacity=0.8,
                  line_opacity=.3,
                  legend_name=f"{param} par commune par departement ",
                  nan_fill_color='white').add_to(m2)

            folium_static(m2)

#                threshold_scale=[-10, 60, 70, 80, 90, 100]
show_maps2(geodf2, threshold(geodf2, param))
folium.LayerControl().add_to(m2)


st.markdown('''# Distribution des biens Fonciers à Marseille''')

typelocal = st.radio(
     "",
     ('Maisons', 'Appartements'))


# Show Marseille Images
from PIL import Image
if typelocal == 'Appartements':
    image = Image.open('boxplot_appartements_Marseille.png')
    st.image(image)
else:
    image2 = Image.open('boxplot_maisons_Marseille.png')
    st.image(image2)
'''
# PRÉDICTION DE LA VALEUR FONCIÈRE
'''
st.markdown('''## Prix/m² en fonction du type de logement
''')
# Minimal necessary data to run our "predict API"
# Minimal necessary data to run our "predict API"
type_local = st.radio(
     "",
     ('Maison', 'Appartement'))

'''
### Surface en m² du bien à estimer?
'''
surface = st.slider('', 0, 500, 25)

"""
### Nombre de pièces principales
"""
pieces = st.slider('', 0, 1, 8)
value = list(range(1, 17))


"""
### Arrondissement
"""
arrondissement = st.selectbox("",
                     value)


dependancy = 0
surface_terrain = 0
arrondissements = np.zeros(16, 'int')
index = (arrondissement + 7) % 16 - 1
arrondissements[index] = 1  #vector of appartement presence concatenated

if type_local == 'Maison':
    local = np.array([0, 1])
else:
    local = np.array([1, 0])

        #vector of appartement presence concatenated
    """Enter the parameters used to execute the predict API,
    to return the price per squared meter"""

data_to_predict = np.concatenate(
        (np.array([surface]), np.array([pieces]), np.array([surface_terrain]),
         np.array([dependancy]), arrondissements, local))
    # X_pred = pd.DataFrame(data_to_predict).T

Arrondissement10=data_to_predict[4]
Arrondissement11=data_to_predict[5]
Arrondissement12=data_to_predict[6]
Arrondissement13=data_to_predict[7]
Arrondissement14=data_to_predict[8]
Arrondissement15=data_to_predict[9]
Arrondissement16=data_to_predict[10]
Arrondissement1=data_to_predict[11]
Arrondissement2=data_to_predict[12]
Arrondissement3=data_to_predict[13]
Arrondissement4=data_to_predict[14]
Arrondissement5=data_to_predict[15]
Arrondissement6=data_to_predict[16]
Arrondissement7=data_to_predict[17]
Arrondissement8=data_to_predict[18]
Arrondissement9=data_to_predict[19]
is_house=data_to_predict[20]
is_appart=data_to_predict[21]

param_dict = {
    "surface_reelle_bati": [int(surface)],
    "nombre_pieces_principales": [int(pieces)],
    "surface_terrain": [int(surface_terrain)],
    "Dependency": [int(dependancy)],
    "Marseille 10e Arrondissement": [int(Arrondissement10)],
    "Marseille 11e Arrondissement": [int(Arrondissement11)],
    "Marseille 12e Arrondissement": [int(Arrondissement12)],
    "Marseille 13e Arrondissement": [int(Arrondissement13)],
    "Marseille 14e Arrondissement": [int(Arrondissement14)],
    "Marseille 15e Arrondissement": [int(Arrondissement15)],
    "Marseille 16e Arrondissement": [int(Arrondissement16)],
    "Marseille 1er Arrondissement": [int(Arrondissement1)],
    "Marseille 2e Arrondissement": [int(Arrondissement2)],
    "Marseille 3e Arrondissement": [int(Arrondissement3)],
    "Marseille 4e Arrondissement": [int(Arrondissement4)],
    "Marseille 5e Arrondissement": [int(Arrondissement5)],
    "Marseille 6e Arrondissement": [int(Arrondissement6)],
    "Marseille 7e Arrondissement": [int(Arrondissement7)],
    "Marseille 8e Arrondissement": [int(Arrondissement8)],
    "Marseille 9e Arrondissement": [int(Arrondissement9)],
    "Appartement": [int(is_house)],
    "Maison": [int(is_appart)]
    }
url = "https://reestimatordocker-jw6jz6q2fq-ew.a.run.app"
if st.button('Prix estimé'):
    response = requests.get(url, params=param_dict).json()
    col1, col2 = st.columns(2)
    col2.metric("", f"{response['prediction']}€")
