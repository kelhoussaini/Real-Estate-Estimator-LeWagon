from reestimator.Mysql_mgmt.get_data import Data_loading
#Importing our Packages: Analytics
import pandas as pd
import numpy as np

#Viz libaries
import matplotlib.pyplot as plt
import seaborn as sns
import plotly as ply

#Web App Libraries
from streamlit_folium import folium_static
import requests

#Create String for data creation
querystring = """SELECT dwu.code_commune AS code,
dwu.type_local AS type,   
dwu.nom_commune AS commune,
dwu.code_postal AS Code_post,
ROUND(AVG(dwu.valeur_fonciere/dwu.surface_reelle_bati),0) AS Prixm2,
ROUND(AVG(dwu.valeur_fonciere),0) AS Price,
ROUND(AVG(dwu.surface_reelle_bati),0) AS Avg_sqm,
COUNT(dwu.id_mutation) AS transactions,
MAX(dwu.latitude) AS lat,
MAX(dwu.longitude) AS lon
FROM data_working_update dwu
WHERE dwu.type_local IN('Appartement', 'Maison')
GROUP BY code_commune, Code_post, nom_commune, dwu.type_local;
"""

#Obtain Our data for the app
getting_data = Data_loading()
df = getting_data.get_data(querystring)
url = 'https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/communes-version-simplifiee.geojson'
response =  requests.get(url).json()
df2 = df[df['type'] == 'Appartement']
geodf = df2[['commune','transactions']]

#Group Paris, Marseille, Lyon by arrondissement
def transform_string(string, separator):
    L = string.split(separator)
    return L[0] if L[0] in ['Paris', 'Marseille', 'Lyon'] else L[0]
geodf.commune = geodf.commune.apply(lambda x: transform_string(x,' '))
geodf = geodf.groupby(geodf.commune).sum().reset_index(drop=False)

# import the folium library
import folium

# initialize the map and store it in a m object
m = folium.Map(location=[46.514783, 6.163627], zoom_start=4)

# show the map
folium.Choropleth(
    geo_data=response,
    name="choropleth",
    data=geodf,
    columns=["commune", "transactions"],
    key_on= "feature.properties.nom",
    fill_color="OrRd",
    fill_opacity=0.8,
    line_opacity=.01,
    legend_name="transaction par commune",
    nan_fill_color='white'
).add_to(m)

folium.LayerControl().add_to(m)

folium_static(m)