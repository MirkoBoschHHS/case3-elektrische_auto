import plotly.figure_factory as ff
import folium
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np



breed = 1000
hoog = 500

def histogram_laadtijd_elek_auto(laadpaal_data):
    fig = ff.create_distplot([laadpaal_data['ConnectedTime'], laadpaal_data['ChargeTime']],
                             group_labels=['Aangesloten tijd', 'Laadtijd'],
                             bin_size=0.25,  # elke bin komt overeen met 15 minuten
                             show_rug=False,
                             curve_type='kde',
                             histnorm='probability density',
                             colors=['mediumblue', 'dodgerblue'])

    annotation_gem1 = {'xref': 'paper',
                       'yref': 'paper',
                       'x': 0.98,
                       'y': 0.89,
                       'showarrow': False,
                       'text': '<b>Gemiddelde laadtijd: ' + str(round(laadpaal_data.ChargeTime.mean(), 2)) + ' uur</b>',
                       'font': {'size': 13, 'color': 'black'}}

    annotation_mediaan1 = {'xref': 'paper',
                           'yref': 'paper',
                           'x': 0.98,
                           'y': 0.83,
                           'showarrow': False,
                           'text': '<b>Mediaan laadtijd: ' + str(
                               round(laadpaal_data.ChargeTime.median(), 2)) + ' uur</b>',
                           'font': {'size': 13, 'color': 'black'}}

    annotation_gem2 = {'xref': 'paper',
                       'yref': 'paper',
                       'x': 0.98,
                       'y': 0.67,
                       'showarrow': False,
                       'text': '<b>Gemiddelde aangesloten tijd: ' + str(
                           round(laadpaal_data.ConnectedTime.mean(), 2)) + ' uur</b>',
                       'font': {'size': 13, 'color': 'black'}}

    annotation_mediaan2 = {'xref': 'paper',
                           'yref': 'paper',
                           'x': 0.98,
                           'y': 0.58,
                           'showarrow': False,
                           'text': '<b>Mediaan aangesloten tijd: ' + str(
                               round(laadpaal_data.ConnectedTime.median(), 2)) + ' uur</b>',
                           'font': {'size': 13, 'color': 'black'}}

    fig.update_layout({'annotations': [annotation_gem1, annotation_mediaan1, annotation_gem2, annotation_mediaan2],
                       'title': "Histogram laad- en aangesloten tijd elektrische auto's met benadering kansdichtheidsfunctie",
                       'xaxis': {'range': [0, 8]}})

    fig.update_layout(xaxis=dict(
        rangeslider=dict(visible=True)))

    fig.update_xaxes(title_text='Tijd in uren')
    fig.update_yaxes(title_text='Dichtheid')
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )

    return fig



#---------------------------------------------------


def color_producer(type):
    if type == 'Ecotap':
        return 'Black'
    if type == 'Allego BV':
        return 'dimgray'
    if type == '(Unknown Operator)':
        return 'silver'
    if type == 'Shell UK Oil Products Limited':
        return 'rosybrown'
    if type == 'Ionity':
        return 'brown'
    if type == 'EV-Box':
        return 'darkred'
    if type == 'Tesla Motors (Worldwide)':
        return 'salmon'
    if type == 'Alfen':
        return 'orangered'
    if type == 'nan':
        return 'sienna'
    if type == 'Vattenfall InCharge':
        return 'saddlebrown'
    if type == 'Greenflux':
        return 'peru'
    if type == 'Last Mile Solutions':
        return 'darkorange'
    if type == 'Eneco':
        return 'burlywood'
    if type == '(Private Residence/Individual)':
        return 'moccasin'
    if type == 'Nuon':
        return 'darkgoldenrod'
    if type == 'FastNed':
        return 'gold'
    if type == 'Blue Marble Charging':
        return 'khaki'
    if type == 'Park & Charge (D)':
        return 'olive'
    if type == 'Incharge':
        return 'yellow'
    if type == 'Park & Charge (CH)':
        return 'yellowgreen'
    if type == 'Lidl':
        return 'darkolivergreen'
    if type == 'The New Motion (NL)':
        return 'chartreuse'
    if type == '(Business Owner at Location)':
        return 'darkseagreen'
    if type == 'TOTAL Nl PlugToDrive':
        return 'lightgreen'
    if type == 'EV-Point':
        return 'lime'
    if type == 'EVnetNL':
        return 'springgreen'
    if type == 'e-Laad':
        return 'aquamarine'
    if type == 'Blue Corner (Belgium)':
        return 'turquoise'
    if type == 'The New Motion (BE)':
        return 'lightseagreen'
    if type == 'ThePluginCompany (Belgium)':
        return 'darkslategray'
    if type == 'MisterGreen, The Fast Charger Network':
        return 'aqua'
    if type == 'eNovates':
        return 'cadetblue'
    if type == 'POD Point (UK)':
        return 'deepskyblue'
    if type == 'Nomadpower':
        return 'dodgerblue'
    if type == 'ChargePoint (Coulomb Technologies)':
        return 'cornflowerblue'
    if type == 'Essent (NL)':
        return 'navy'
    if type == 'FLOW Charging':
        return 'slateblue'
    if type == 'Stadtwerke Clausthal-Zellerfeld':
        return 'indigo'
    if type == 'RWE Mobility/Essent':
        return 'darkviolet'

def add_categorical_legend(folium_map, title, colors, labels):
    if len(colors) != len(labels):
        raise ValueError("colors and labels must have the same length.")

    color_by_label = dict(zip(labels, colors))

    legend_categories = ""
    for label, color in color_by_label.items():
        legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"

    legend_html = f"""
    <div id='maplegend' class='maplegend'>
      <div class='legend-title'>{title}</div>
      <div class='legend-scale'>
        <ul class='legend-labels'>
        {legend_categories}
        </ul>
      </div>
    </div>
    """
    script = f"""
        <script type="text/javascript">
        var oneTimeExecution = (function() {{
                    var executed = false;
                    return function() {{
                        if (!executed) {{
                             var checkExist = setInterval(function() {{
                                       if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                          document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                          clearInterval(checkExist);
                                          executed = true;
                                       }}
                                    }}, 100);
                        }}
                    }};
                }})();
        oneTimeExecution()
        </script>
      """

    css = """

    <style type='text/css'>
      .maplegend {
        z-index:9999;
        float:right;
        background-color: rgba(255, 255, 255, 1);
        border-radius: 5px;
        border: 2px solid #bbb;
        padding: 10px;
        font-size:12px;
        positon: relative;
      }
      .maplegend .legend-title {
        text-align: left;
        margin-bottom: 5px;
        font-weight: bold;
        font-size: 90%;
        }
      .maplegend .legend-scale ul {
        margin: 0;
        margin-bottom: 5px;
        padding: 0;
        float: left;
        list-style: none;
        }
      .maplegend .legend-scale ul li {
        font-size: 80%;
        list-style: none;
        margin-left: 0;
        line-height: 18px;
        margin-bottom: 2px;
        }
      .maplegend ul.legend-labels li span {
        display: block;
        float: left;
        height: 16px;
        width: 30px;
        margin-right: 5px;
        margin-left: 0;
        border: 0px solid #ccc;
        }
      .maplegend .legend-source {
        font-size: 80%;
        color: #777;
        clear: both;
        }
      .maplegend a {
        color: #777;
        }
    </style>
    """

    folium_map.get_root().header.add_child(folium.Element(script + css))

    return folium_map

def map_folium(response_dataframe, max_results):
    sw = response_dataframe[['AddressInfo.Latitude', 'AddressInfo.Longitude']].quantile(0.05).values.tolist()
    ne = response_dataframe[['AddressInfo.Latitude', 'AddressInfo.Longitude']].quantile(0.95).values.tolist()

    m = folium.Map(tiles='Carto DB Positron')#location=[average_lat, average_lon], zoom_start=zoom)

    # Expres gebruik gemaakt van Circle
    # nu worden die circles niet enorm groot bij het uitzoemen
    # Als je inzoom zie ook dat ze verschillende radius hebben

    bar = st.progress(0)
    i = 0

    for row in response_dataframe.iterrows():
        row_values = row[1]
        location = [row_values['AddressInfo.Latitude'], row_values['AddressInfo.Longitude']]
        marker_location = row_values['AddressInfo.Town']
        marker = folium.Circle(location=location,
                               fill=True,
                               fill_color=color_producer(row_values['OperatorInfo.Title']),
                               color=color_producer(row_values['OperatorInfo.Title']),
                               popup='<strong>' + str(row_values['OperatorInfo.Title']) + '</strong>',
                               )
        marker.add_to(m)

        i += 1
        value = int(i / ((max_results / 100)))
        if(value > 98):
            value = 98
        bar.progress(value)



    m.fit_bounds([sw, ne]) # Center map
    return m ,bar



#---------------------------------------------------


def lijn(autos_per_maand_cum):
    autos_per_maand_cum.reset_index(drop=False, inplace=True)
    autos_per_maand_cum['Jaar'] = autos_per_maand_cum['Tijd in jaren'].astype(int)
    autos_per_maand_cum['Maand'] = (
                (autos_per_maand_cum['Tijd in jaren'] - autos_per_maand_cum['Jaar'] + 1 / 12) * 12).astype(int)
    autos_per_maand_cum.rename(columns={'Teller': "Aantal auto's"}, inplace=True)

    fig = px.line(autos_per_maand_cum,
                  x='Tijd in jaren',
                  y="Aantal auto's",
                  line_group='Brandstof',
                  color='Brandstof',
                  hover_data={'Tijd in jaren': False, 'Brandstof': True, "Aantal auto's": True, 'Jaar': True,
                              'Maand': True},
                  title="Lijndiagram cumulatieve som aantal auto's per brandstofcategorie vs. tijd in jaren")
    fig.update_layout(xaxis=dict(
        rangeslider=dict(visible=True), range=[1995, 2022]))
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )
    del autos_per_maand_cum
    return fig


#---------------------------------------------------

def percentage_auto_soort(autos_per_maand_cum):
    rdw_data_select = autos_per_maand_cum.loc[:,['Tijd in jaren','Brandstof',"Aantal auto's"]]
    data = rdw_data_select.pivot(index='Tijd in jaren', columns='Brandstof', values="Aantal auto's")
    data['Overig'] = data['Overig'].fillna(0)
    data["% Elektrische auto's"] = data['Elektriciteit'] / (data['Benzine']+data['Diesel']+data['Elektriciteit']+data['LPG']+data['Overig']) * 100
    data["% Benzine auto's"] = data['Benzine'] / (data['Benzine']+data['Diesel']+data['Elektriciteit']+data['LPG']+data['Overig']) * 100
    data["% Diesel auto's"] = data['Diesel'] / (data['Benzine']+data['Diesel']+data['Elektriciteit']+data['LPG']+data['Overig']) * 100
    data["% LPG auto's"] = data['LPG'] / (data['Benzine']+data['Diesel']+data['Elektriciteit']+data['LPG']+data['Overig']) * 100
    data["% Overig auto's"] = data['Overig'] / (data['Benzine']+data['Diesel']+data['Elektriciteit']+data['LPG']+data['Overig']) * 100
    data['controle'] = data["% Elektrische auto's"] + data["% Benzine auto's"] + data["% Diesel auto's"] + data["% LPG auto's"] + data["% Overig auto's"]

    fig = px.line(data, x=data.index, y=["% Benzine auto's", "% Diesel auto's",
    "% Elektrische auto's", "% LPG auto's",
    "% Overig auto's"],
    title="Percentage auto soort van het totaal aantal auto's in Nederland")# Dropdown menu
    dropdown_buttons=[{'label': 'Alle', 'method': 'update','args':[{'visible': [True, True, True, True, True]}]},
    {'label': 'Benzine', 'method': 'update','args':[{'visible': [True, False, False, False, False]}]},
    {'label': 'Diesel', 'method': 'update','args':[{'visible': [False, True, False, False, False]}]},
    {'label': 'Elektrische', 'method': 'update','args':[{'visible': [False, False, True, False, False]}]},
    #{'label': 'LPG', 'method': 'update','args':[{'visible': [False, False, False, True, False]}]},
    #{'label': 'Overig', 'method': 'update','args':[{'visible': [False, False, False, False, True]}]}
    ]
    fig.update_layout({'updatemenus':[{'type': "dropdown",'x':1.172,'y':0.65,'showactive': True,'buttons': dropdown_buttons}]})
    fig.update_yaxes(title_text='Percentage auto soort')
    fig.update_layout(title_x=0.5)
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )
    fig.update_layout(xaxis=dict(
        rangeslider=dict(visible=True, range=[2004,202]), range=[2004, 2022]))
    return fig
    # fig.show()

#---------------------------------------------------

def spreiding(rdw_data):
    elektrisch = rdw_data[rdw_data['Brandstof'] == 'Elektriciteit'][['Tijd in jaren', 'Teller']]
    fossiel = rdw_data[rdw_data['Brandstof'] != 'Elektriciteit'][['Tijd in jaren', 'Teller']]
    elektrisch = pd.DataFrame(elektrisch.groupby('Tijd in jaren')['Teller'].sum())
    elektrisch.reset_index(drop=False, inplace=True)
    elektrisch = elektrisch[elektrisch['Tijd in jaren'] >= 2004]
    elektrisch.reset_index(drop=True, inplace=True)
    fossiel = pd.DataFrame(fossiel.groupby('Tijd in jaren')['Teller'].sum())
    fossiel.reset_index(drop=False, inplace=True)
    fossiel = fossiel[fossiel['Tijd in jaren'] >= 2004]
    fossiel.reset_index(drop=True, inplace=True)
    elektrisch['Verhouding'] = elektrisch['Teller'] / fossiel['Teller']
    elektrisch['Verhouding log'] = np.log(elektrisch['Verhouding'])

    fig = px.scatter(data_frame=elektrisch,
                     x='Tijd in jaren',
                     y='Verhouding log',
                     trendline='ols',
                     hover_data={'Verhouding': True},
                     title="Spreidingsdiagram van de verhouding elektrische / niet-elektrische auto's vs. de tijd met regressielijn",
                     trendline_color_override='red',
                     color_discrete_sequence=px.colors.qualitative.Prism,
                     labels={'Verhouding log': "Natuurlijk logaritme verhouding elektrisch / niet-elektrisch",
                             'Verhouding': "Verhouding elektrisch / niet-elektrisch"})
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )
    return fig

#---------------------------------------------------

def voorspelling():
    def voorspellen(jaartal):
        verhouding = np.exp(-512.538 + 0.252867 * jaartal)
        percentage = round((verhouding / (verhouding + 1)) * 100, 1)
        return percentage

    voorspellingen = pd.DataFrame()

    for i in range(2022, 2051):
        voorspellingen.loc[i - 2022, 'Jaartal'] = i
        voorspellingen.loc[i - 2022, 'Voorspelling'] = voorspellen(i)
    voorspellingen['Jaartal'] = voorspellingen['Jaartal'].astype(int)

    fig = px.line(data_frame=voorspellingen,
                  x='Jaartal',
                  y='Voorspelling',
                  labels={'Voorspellingen': "Voorspeld % elekrische auto's",
                          'Jaartal': "Tijd in jaren"},
                  color_discrete_sequence=px.colors.qualitative.Prism,
                  title="Lijndiagram van het voorspelde % elektrische auto's vs. de tijd")

    annotation1 = {
        'x': 2027,
        'y': 50.6,
        'showarrow': True,
        'text': '<b>2027: 50,6 %</b>',
        'font': {'size': 12, 'color': 'black'},
        'arrowhead': 5}

    annotation2 = {
        'x': 2032,
        'y': 78.4,
        'showarrow': True,
        'text': '<b>2032: 78,4 %</b>',
        'font': {'size': 12, 'color': 'black'},
        'arrowhead': 5}

    annotation3 = {
        'x': 2039,
        'y': 95.5,
        'showarrow': True,
        'text': '<b>2039: 95,5 %</b>',
        'font': {'size': 12, 'color': 'black'},
        'arrowhead': 5}

    fig.update_layout({'annotations': [annotation1, annotation2, annotation3]})
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )
    return fig


def bar_chart_laadpalen(openCharge):
    openChargeFiltered = openCharge[['AddressInfo.Town', 'NumberOfPoints', 'DateCreated', 'OperatorInfo.Title']]
    openChargeFilteredDropped = openChargeFiltered.dropna(
        subset=['AddressInfo.Town', 'NumberOfPoints', 'DateCreated', 'OperatorInfo.Title'])
    openChargeFilteredDropped["NumberOfPoints"] = openChargeFilteredDropped["NumberOfPoints"].fillna(0).astype(int)
    openChargeFilteredDropped = openChargeFilteredDropped.rename(columns={"OperatorInfo.Title": "Title"})

    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "(Unknown Operator)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "(Business Owner at Location)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[
        openChargeFilteredDropped.Title == "ChargePoint (Coulomb Technologies)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "e-Laad", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Vattenfall InCharge", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Vattenfall InCharge", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "FLOW Charging", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Nomadpower", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Ionity", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "ThePluginCompany (Belgium)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Last Mile Solutions", "Title"] = "Overig"
    openChargeFilteredDropped.loc[
        openChargeFilteredDropped.Title == "(Private Residence/Individual)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Lidl", "Title"] = "Overig"
    openChargeFilteredDropped.loc[
        openChargeFilteredDropped.Title == "MisterGreen, The Fast Charger Network", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Blue Corner (Belgium)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "TOTAL Nl PlugToDrive", "Title"] = "Overig"
    openChargeFilteredDropped.loc[
        openChargeFilteredDropped.Title == "Shell UK Oil Products Limited", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "RWE Mobility/Essent", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "POD Point (UK)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[
        openChargeFilteredDropped.Title == "Shell UK Oil Products Limited", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Eneco", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Blue Marble Charging", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Incharge", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Park & Charge (D)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Park & Charge (CH)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "eNovates ", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "EV-Point", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "Greenflux", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "The New Motion (NL)", "Title"] = "Overig"
    openChargeFilteredDropped.loc[openChargeFilteredDropped.Title == "eNovates"] = "Overig"


    gemeentes = pd.read_csv('gemeentes.csv', sep=";")
    gemeenteDorp = gemeentes.drop_duplicates(subset=['Gemeente'])

    openChargeFilteredDropped['AddressInfo.Town'] = openChargeFilteredDropped['AddressInfo.Town'].str.strip()
    gemeenteDorp['Gemeente'] = gemeenteDorp['Gemeente'].str.strip()

    GraphData = openChargeFilteredDropped.merge(gemeenteDorp, how='left', left_on='AddressInfo.Town', right_on='Gemeente')

    GraphDataGrouped = GraphData.groupby(['Provincie', 'Title'], as_index=False).sum()
    GraphD = pd.DataFrame(GraphDataGrouped)
    GraphD = GraphD.sort_values(["NumberOfPoints"], ascending=False)
    pd.set_option('display.max_rows', None)

    fig = px.bar(GraphD,
                 x="Provincie",
                 y="NumberOfPoints",
                 color="Title",
                 title="Laadpalen verspreid over Nederland per provincie",
                 labels={"NumberOfPoints": "Aantal laadpunten", "Provincie": "Provincies", "Title": "Providers"})
    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )
    return fig


def lijn_laadpalen(openCharge):
    openChargeFiltered = openCharge[['AddressInfo.Town', 'NumberOfPoints', 'DateCreated', 'OperatorInfo.Title']]
    openChargeFilteredDropped = openChargeFiltered.dropna(
        subset=['AddressInfo.Town', 'NumberOfPoints', 'DateCreated', 'OperatorInfo.Title'])

    gemeentes = pd.read_csv('gemeentes.csv', sep=";")
    gemeenteDorp = gemeentes.drop_duplicates(subset=['Gemeente'])

    openChargeFilteredDropped['AddressInfo.Town'] = openChargeFilteredDropped['AddressInfo.Town'].str.strip()
    gemeenteDorp['Gemeente'] = gemeenteDorp['Gemeente'].str.strip()

    GraphData = openChargeFilteredDropped.merge(gemeenteDorp, how='left', left_on='AddressInfo.Town',
                                                right_on='Gemeente')
    GraphData = GraphData.dropna(subset=['Provincie', 'NumberOfPoints', 'DateCreated'])

    GraphData = GraphData[['Provincie', 'DateCreated', 'NumberOfPoints']]

    GraphData = GraphData.sort_values(["DateCreated", "Provincie"], ascending=True)

    GraphData['Grouped Cumulative Sum'] = GraphData[['Provincie', 'NumberOfPoints']].groupby('Provincie').cumsum()

    fig = px.line(GraphData, x="DateCreated", y="Grouped Cumulative Sum", color="Provincie",
                  labels={"DateCreated": "Datum in gebruik", "Provincie": "Provincies",
                          "Grouped Cumulative Sum": "Totaal aantal laadpalen"})

    fig.update_traces(textposition="bottom right")

    fig.update_layout(
        autosize=False,
        width=breed,
        height=hoog, )

    return fig


