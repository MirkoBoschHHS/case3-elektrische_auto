import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.figure_factory as ff
import plotly.express as px
import io
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from streamlit_folium import folium_static
import folium
from glob import glob

import Get_data
import Figuren

# Enkele standaard opties
st.set_page_config(layout="wide") # Zorgt voor default wide op streamlit
pd.set_option('display.max_columns', None) # Print alles van de DataFrame pandas

# Get secrets
try:
    max_results = st.secrets["max_results"]
except:
    max_results = 80

# Maak een titel
st.title('Dashboard elektrische auto\'s')


# Get data from API / CSV
laadpaal_data = Get_data.load_csv_laadpaal_data('laadpaaldata.csv')




def print_text(file_nr):
    try:
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)

        files = str(glob('Text_bestanden/' + str(file_nr) + ' -*'))
        file = files.split("\\")[-1].replace("\"]", "").replace("']", "")
        title = file.replace(".txt", "").split("-")[-1]

        with open('Text_bestanden/' + file) as f:
            lines = f.readlines()

        return title, lines
    except:
        return "NO TITLE", "NO TEXT"
    # for row in lines:
    #     col.write(row)




# ---------- Histogram van laadtijd ----------
title, lines = print_text(1)
st.header(title)
col1, col2 = st.columns([1,2])
for row in lines:
    col1.write(row)
col2.plotly_chart(Figuren.histogram_laadtijd_elek_auto(laadpaal_data))



st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
title, lines = print_text(2)
st.header(title)
col1, col2 = st.columns([1,2])
response_dataframe, country = Get_data.OpenChargeMap(col1, max_results)


providers = response_dataframe['OperatorInfo.Title'].unique()

provider_choice = col1.multiselect(
    "Kies een provider", providers, providers)

response_dataframe_choice = response_dataframe.loc[response_dataframe['OperatorInfo.Title'].isin(provider_choice)]

m, bar = Figuren.map_folium(response_dataframe_choice, max_results)

# print_text(col1, '2 - Waar bevinden openbare laadstations van Open Chargemap.txt')
for row in lines:
    col1.write(row)

bar.progress(99)
with col2:
    folium_static(m)
bar.progress(100)
bar.empty()



st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
title, lines = print_text(3)
st.header(title)
col1, col2 = st.columns([1,2])
autos_per_maand_cum, rdw_data = Get_data.rdw_data()
fig = Figuren.lijn(autos_per_maand_cum)
col2.write("Plotting figure...")
col2.plotly_chart(fig)
for row in lines:
    col1.write(row)


st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
title, lines = print_text(4)
st.header(title)
col1, col2 = st.columns([1,2])
col1.write("Hier nog een tekst of interactie")
col2.plotly_chart(Figuren.percentage_auto_soort(autos_per_maand_cum))
for row in lines:
    col1.write(row)


st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
title, lines = print_text(5)
st.header(title)
col1, col2 = st.columns([1,2])
col2.plotly_chart(Figuren.spreiding(rdw_data))
for row in lines:
    col1.write(row)



st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
title, lines = print_text(6)
st.header(title)
col1, col2 = st.columns([1,2])
col2.plotly_chart(Figuren.voorspelling())
for row in lines:
    col1.write(row)

if(country == "NL"):
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    title, lines = print_text(7)
    st.header(title)
    col1, col2 = st.columns([1,2])
    col2.plotly_chart(Figuren.bar_chart_laadpalen(response_dataframe))
    col2.plotly_chart(Figuren.lijn_laadpalen(response_dataframe))
    for row in lines:
        col1.write(row)




