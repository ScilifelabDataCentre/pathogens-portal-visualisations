"""Maps values onto a county-level map of Sweden"""
import json
import pandas as pd
import plotly.express as px
import csv
import requests

#map
with open('sverige-lan-counties-of-sweden.geojson', 'r') as sw:
  data = json.load(sw)

#to check the properties of your geojson
# for f in jdata['features'][:5]:
#     print(f['properties'])

#dictionary to match data and map
counties_id_map = {}
for feature in jdata['features']:
  feature['id'] = feature['properties']['id']
  counties_id_map[feature['properties']['lan_namn']] = feature['id']

#data
req = requests.get('https://urls.dckube.scilifelab.se/goto/csss/')
reader = csv.reader(req.text.splitlines())
data = list(reader)[-21:]
df1 = pd.DataFrame(data[0:], columns = ['Lan', 'Datum',
                                        'Uppskattning', 'Low_CI', 'High_CI'])

#format data
df1['Datum'] = pd.to_datetime(df1['Datum'])
df1.sort_values(by = 'Datum', ascending = False, inplace = True)
df1.drop_duplicates('Lan', keep = 'first', inplace = True)
df1['Uppskattning'] = pd.to_numeric(df1['Uppskattning'], errors = 'coerce')
df1['Uppskattning'] = df1['Uppskattning'].fillna(-0.1)
#comment out next row when Dalarna fixed
df1['Lan'] = df1['Lan'].replace('Dalar', 'Dalarna')
df1['Lan'] = df1['Lan']+'s län'
df1['Lan'] = df1['Lan'].replace('Skånes län', 'Skåne län')
df1['Lan'] = df1['Lan'].replace('Blekinges län', 'Blekinge län')
df1['Lan'] = df1['Lan'].replace('Örebros län', 'Örebro län')
df1['Lan'] = df1['Lan'].replace('Kalmars län', 'Kalmar län')
df1['Lan'] = df1['Lan'].replace('Uppsalas län', 'Uppsala län')
df1['id'] = df1['Lan'].apply(lambda x: counties_id_map[x])

#bin the data to create discrete colour options
bins = [-0.20, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 10.0]
labels = ['Otillräckligt underlag', '0.00-0.10 %', '0.10-0.20 %', '0.20-0.30 %',
        '0.30-0.40 %', '0.40-0.50 %', '0.50-0.60 %', '0.60-0.70 %',
        '0.70-0.80 %', '0.80-0.90 %', '>0.90 %']
df1['binned'] = pd.cut(df1['Uppskattning'], bins = bins, labels = labels)
df1.sort_values('binned', ascending = False, inplace = True)

#make figure
fig = px.choropleth(df1, geojson = jdata,
                    locations = 'id',
                    color = df1['binned'],
                    color_discrete_map = {'Otillräckligt underlag':'black',
                                    '0.00-0.10 %':px.colors.sequential.tempo[0],
                                    '0.10-0.20 %':px.colors.sequential.tempo[1],
                                    '0.20-0.30 %':px.colors.sequential.tempo[2],
                                    '0.30-0.40 %':px.colors.sequential.tempo[3],
                                    '0.40-0.50 %':px.colors.sequential.tempo[4],
                                    '0.50-0.60 %':px.colors.sequential.tempo[5],
                                    '0.60-0.70 %':px.colors.sequential.tempo[6],
                                    '0.70-0.80 %':px.colors.sequential.tempo[7],
                                    '0.80-0.90 %':px.colors.sequential.tempo[8],
                                    '>0.90 %':px.colors.sequential.tempo[9]},
                    scope = 'europe',
                    hover_name = 'Lan',
                    hover_data = ['Uppskattning'])

fig.update_geos(fitbounds = 'locations',
                visible = False)
fig.update_layout(margin = {'r':0, 't':0, 'l':0, 'b':0},
                width = 1000, height = 1000)
fig.update_layout(legend_title_text = '<b>Uppskattning</b>',
                dragmode = False)
fig.update_layout(legend = dict(x = 0.65, y = 1))

#to 'show' the figure in browser
#fig.show()
#to write the file as .png
#fig.write_image('map_with_factor.png', scale=2)
#write out as html for web
#fig.write_html('map_with_factor.html', include_plotlyjs=False, full_html=False)
