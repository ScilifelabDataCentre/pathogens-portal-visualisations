"""Outputs numbers of total publications with headers,
shows overall number of publications and total publications
associated with each funder"""

import plotly.graph_objects as go
import requests

#get data
res=requests.get('https://publications-covid19.scilifelab.se/publications.json')
overall = res.json()
res1=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab.json')
SLL = res1.json()
res2=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20Vinnova.json')
Vin = res2.json()
res3=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20VR%3A%20Special%20COVID-19%20funding.json')
VRS = res3.json()
res4=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20VR.json')
VR = res4.json()
res5=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20NordForsk.json')
NF = res5.json()
res6=requests.get('https://publications-covid19.scilifelab.se/label/Funder%3A%20H2020.json')
H20 = res6.json()

fig = go.Figure()

fig.add_trace(go.Indicator(
    mode='number',
    value=overall['publications_count'],
    title={'text': '<b>Total Publications in Database</b>'},
    delta={'reference': 400, 'relative': True, 'position':'top'},
    number={'font':{'size':70}},
    domain={'x':[0, 0.5], 'y':[0.5, 1]}
))


fig.add_trace(go.Indicator(
    mode='number',
    value=SLL['publications_count'],
    title={'text': '<b>Total Publications Funded by KAW/SciLifeLab</b>'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.999, 1]}
))

fig.add_trace(go.Indicator(
    mode='number',
    value=Vin['publications_count'],
    title={'text': '<b>Total Publications Funded by Vinnova'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.8, 1]}
))

fig.add_trace(go.Indicator(
    mode='number',
    value=VRS['publications_count'],
    title={'text':
        '<b>Total Publications Funded byVR Special COVID-19 Funding</b>'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.6, 1]}
))

fig.add_trace(go.Indicator(
    mode='number',
    value=VR['publications_count'],
    title={'text': '<b>Total Publications Funded by VR</b>'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.4, 1]}
))

fig.add_trace(go.Indicator(
    mode='number',
    value=NF['publications_count'],
    title={'text': '<b>Total Publications Funded by NordForsk</b>'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.2, 1]}
))


fig.add_trace(go.Indicator(
    mode='number',
    value=H20['publications_count'],
    title={'text': '<b>Total Publications Funded by H2020</b>'},
    delta={'reference': 200, 'relative': True},
    number={'font':{'size':30}},
    domain={'x':[0.5, 1], 'y':[0.0, 1]}
))

fig.update_layout(height=600, width=600,
                margin={'l':0, 'r':0, 't':50, 'b':0})
#to 'show' the figure in browser
#fig.show()
#to write the file as .png
#fig.write_image('publication_num_ind.png', scale=2)
#write out as html for web
#fig.write_html('publication_num_ind.html',
#               include_plotlyjs=False, full_html=False
