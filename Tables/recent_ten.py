"""This script produces a table showing
the most recent 10 publications in the COVID-19
publications database"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests

#get data
res=requests.get('https://publications-covid19.scilifelab.se/publications.json')
txt = res.json()
#into dataframe
df = pd.json_normalize(txt['publications'])
df = df[['title', 'authors', 'published', 'doi']].head(20)
#shorten title
df['title']=[x[:60] for x in df['title']]
df['title'] = df['title']+'...'
#sort date to filter to before today and 10 most recent
#below line assumes 1st when no day is given in date
df.replace('-00', '-01', regex = True, inplace = True)
df['Published'] = pd.to_datetime(df['published'], format = '%Y-%m-%d').dt.date
df = df[df['Published']<pd.to_datetime('today').date()]
df = df[['title', 'authors', 'Published', 'doi']].head(10)
#make doi links
df['Title'] = '<a href="https://doi.org/'+df['doi']+'">'+df['title']+'</a>'
#combine author names
df['authorscount'] = df['authors'].astype(str).str.count('{')
df['fauth'] = df['authors'].str[0].astype(str).str.split(',').str[0].str.title()
df['sauth'] = df['authors'].str[1].astype(str).str.split(',').str[0].str.title()
df = df.replace(['{\'Family\': ', '\''], ['', ''], regex=True)
df['authors'] = np.where(df['authorscount'] == 2,
                        df['fauth'] + ' and ' + df['sauth'], df['fauth'])
df['Authors'] = np.where(df['authorscount'] > 2,
                        df['fauth'] + ' et al.' , df['authors'])
df['Altmetrics'] = 'altmetrics'
df = df[['Published', 'Authors', 'Title', 'Altmetrics']]

oddrowcol = '#ffffff'
evenrowcol = '#deebf7'
headercol = '#2e68a5'
headertextcol = '#ffffff'
bodytextcol = '#2f4f4f'

fig = go.Figure(data = [go.Table(columnwidth=[250, 250, 700, 200],
    header = dict(
            values = ['<b>Publiation Date</b>', '<b>Authors</b>',
                        '<b>Title</b>', '<b>Altmetrics</b>'],
            align = ['center', 'left', 'left', 'center'],
            fill_color = headercol,
            font = dict(color = headertextcol, size = 14),
            line = dict(width = 0)),
    cells = dict(values = (df['Published'], df['Authors'],
                            df['Title'], df['Altmetrics']),
            align = ['center', 'left', 'left', 'center'],
            fill_color = [[oddrowcol, evenrowcol]*10],
            font = dict(
            color = bodytextcol, size=12),
            height = 30,
            line = dict(width = 0)))])

# to show in broswer. NB- write functions wont work if active
#fig.show()
# change 'include_plotlyjs' to 'true' to enable opening in browser
#write out as html
fig.write_html('Newest_10_pubs.html', include_plotlyjs=False, full_html=False)
