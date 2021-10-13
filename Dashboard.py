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




def print_text(file, col):
    # files = str(glob('Text_bestanden/' + str(file)))
    # file = files.split("\\")[-1].replace("\"]", "").replace("']", "")
    # title = file.replace(".txt", "").split("-")[-1]

    with open('Text_bestanden/' + file) as f:
        lines = f.readlines()

    for row in lines:
        col.write(row)




# ---------- Histogram van laadtijd ----------
st.header("Verdeling laadtijden")
col1, col2 = st.columns([1,2])
print_text("1 - Laadtijd auto.txt", col1)
col2.plotly_chart(Figuren.histogram_laadtijd_elek_auto(laadpaal_data))


if True:
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    st.header("Locatie laadpalen")
    col1, col2 = st.columns([1,2])
    response_dataframe, country = Get_data.OpenChargeMap(col1, max_results)


    providers = response_dataframe['OperatorInfo.Title'].unique()

    provider_choice = col1.multiselect(
        "Kies een provider", providers, providers)

    # response_dataframe_choice = response_dataframe.loc[response_dataframe['OperatorInfo.Title'].isin(provider_choice)]

    m, bar = Figuren.map_folium(response_dataframe.loc[response_dataframe['OperatorInfo.Title'].isin(provider_choice)], max_results)

    # print_text(col1, '2 - Laadtijd auto.txt')
    print_text("2 - Laadtijd auto.txt", col1)

    bar.progress(99)
    with col2:
        folium_static(m)
    bar.progress(100)
    bar.empty()



st.markdown("""---""")
# ---------- Voeg de map van locaties toe ----------
st.header("Aantal soorten auto's")
col1, col2 = st.columns([1,2])
autos_per_maand_cum, rdw_data = Get_data.rdw_data()
fig = Figuren.lijn(autos_per_maand_cum)

col2.plotly_chart(fig)
print_text("3 - Lijndiagram cumulatief.txt", col1)


if False:
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    st.header("Verdeling auto soorten")
    col1, col2 = st.columns([1,2])
    col2.plotly_chart(Figuren.percentage_auto_soort(autos_per_maand_cum))
    print_text("4 - Percentage auto.txt", col1)

del autos_per_maand_cum

if False:
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    st.header("Verhouding elektrische/niet-elektrische auto's")
    col1, col2 = st.columns([1,2])
    col2.plotly_chart(Figuren.spreiding(rdw_data))
    print_text("5 - Spreidingsdiagram.txt", col1)

del rdw_data

if True:
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    st.header("Voorspelling percntage elektrische auto's")
    col1, col2 = st.columns([1,2])
    col2.plotly_chart(Figuren.voorspelling())
    print_text("6 - Lijndiagram voorspelling.txt", col1)




if(country == "NL" and False):
    st.markdown("""---""")
    # ---------- Voeg de map van locaties toe ----------
    st.header("Laadpunten verdeling per provincie")
    col1, col2 = st.columns([1,2])
    col2.plotly_chart(Figuren.bar_chart_laadpalen(response_dataframe))
    col2.plotly_chart(Figuren.lijn_laadpalen(response_dataframe))
    print_text("7 - Laadpunten Nederland.txt", col1)
else:
    st.write("Dit is het einde, selecteer landcode NL voor meer. Nu geselecteerd: " + str(country))


st.write("Done")
