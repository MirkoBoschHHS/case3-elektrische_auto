import requests
import json
import pandas as pd
import os
import streamlit as st

countries = ['NL', 'FR', 'DE', 'BE']

response_dataframe = 0


def OpenChargeMap(col, max_results=50):
  global response_dataframe
  # Max results to load with api
  key = "7854aa82-723c-48d4-afb4-3c437a9db1c9"

  # country = col.radio(
  #   "Kies een landcode", countries)#, ["NL"])


  # if not country:
  #       st.error("Please select at least one station.")
  #       return response_dataframe
  # else:
  response_dataframe = pd.DataFrame({})

  country = 'NL'
  # for country_code in country:
  #Get data
  # url = r'https://api.openchargemap.io/v3/poi/?key=7854aa82-723c-48d4-afb4-3c437a9db1c9?output=kml&countrycode=NL&maxresults=2'
  url = r'https://api.openchargemap.io/v3/poi/?key=' + str(key) + '?output=json&countrycode=' + str(country) + '&maxresults=' + str(max_results)
  # url = 'https://api.openchargemap.io/v3/poi/?output=json&countrycode=' + str(country_code) + '&maxresults=' + str(max_results) + '&compact=true&verbose=false&key=' + str(key) + ')'
  response = requests.get(url)
  response_json = json.loads(response.text)
  response_dataframe = pd.concat([response_dataframe, pd.json_normalize(response.json())])
  # st.write(url)
  return response_dataframe, country

@st.cache
def load_csv_laadpaal_data(path):
  # Data inladen
  for i in range(0, 2):
    try:
      laadpaal_data = pd.read_csv(path)
      break
    except:
      if (i == 0): # Try changing directory
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        #st.write("Change directory")
      else: # Could not find
        st.error("Could not find file '" + path + "' on location: " + str(os.getcwd()))
        return None

  # Data inspecteren
  laadpaal_data = laadpaal_data[laadpaal_data.ChargeTime >= 0]
  laadpaal_data['Charge/Connected'] = laadpaal_data.ChargeTime / laadpaal_data.ConnectedTime
  laadpaal_data = laadpaal_data[laadpaal_data['Charge/Connected'] <= 1]


  # Terug sturen van de data
  return laadpaal_data

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def rdw_data():
  # rdw_data = pd.read_csv('rdw_data.csv')
  rdw_data = pd.read_parquet('rdw_data.gzip')
  rdw_data['Tijd in jaren'] = rdw_data['Jaar'] + (rdw_data['Maand'] - 1) / 12
  rdw_data.drop(columns=['Unnamed: 0'], inplace=True)
  rdw_data['Teller'] = 1
  rdw_data[rdw_data['Brandstof'] == 'Elektriciteit'].groupby('Jaar')['Teller'].sum()
  # rdw_data_2004 = rdw_data[rdw_data['Jaar'] >= 2004].copy()
  rdw_data['Brandstof'].value_counts()
  rdw_data.Brandstof = rdw_data.Brandstof.str.replace('CNG', 'Overig')
  rdw_data.Brandstof = rdw_data.Brandstof.str.replace('LNG', 'Overig')
  rdw_data.Brandstof = rdw_data.Brandstof.str.replace('Alcohol', 'Overig')
  rdw_data.Brandstof = rdw_data.Brandstof.str.replace('Waterstof', 'Overig')
  autos_per_maand = pd.DataFrame(rdw_data.groupby(['Tijd in jaren', 'Brandstof'])['Teller'].sum())
  autos_per_maand_cum = pd.DataFrame(autos_per_maand.groupby('Brandstof')['Teller'].cumsum())
  autos_per_maand_cum.rename(columns={'Teller': 'Cumulatief'})

  return autos_per_maand_cum, rdw_data

