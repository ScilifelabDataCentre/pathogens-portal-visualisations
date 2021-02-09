
#importing all necessary modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 
from PIL import Image
import numpy as np
import requests 
from pandas.io.json import json_normalize
import json

#imports the .json from the publications library :
resp = requests.get('https://publications-covid19.scilifelab.se/publications.json')
txt = resp.json()


#the below level of normalisation will give access to abstract and the title - authors requires further 'digging' in the .json 
df=pd.json_normalize(txt["publications"])

title_words = '' 
# add whatever words you'd like to exclude 
stopwords = list(STOPWORDS) + ['None', 's']

#pick the column you want to import words from df.columnname
for val in df.title: 
    val = str(val) 
    tokens = val.split()       
    title_words += " ".join(tokens)+" "

#to make a square shaped wordcloud
mask = np.array(Image.open('/Users/liahu895/Documents/scilifelab/VI/SciLifeLab symbol/POS/Digital/SciLifeLab_symbol_POS.png'))

#COVID portal visual identity 
#add font
font_path = '/Users/liahu895/Documents/scilifelab/COVID portal /IBM_Plex_Sans/IBMPlexSans-Bold.ttf'

# give colours
def multi_color_func(word=None, font_size=None,position=None, orientation=None, font_path=None, random_state=None):
    colors = [[338, 73, 52], [211,56,41], [206,62,50], [208, 7, 46]]
    rand = random_state.randint(0, len(colors) - 1)
    return "hsl({}, {}%, {}%)".format(colors[rand][0], colors[rand][1], colors[rand][2])

wordcloud = WordCloud( 
                background_color ='white', 
                stopwords = stopwords, 
                font_path=font_path,
                mask=mask,
                min_font_size = 14, 
                width=mask.shape[1],
                height =mask.shape[0], 
                collocation_threshold= 50, # 50 threshold sufficient to exclude 'ill covid' which makes little sense as a bigram (pair of words).
                color_func=multi_color_func,
                prefer_horizontal=1,
# This now includes hyphens in punctuation 
                regexp=r'\w(?:[-\w])*\w?',
#max word default is 200, can make more or less be in cloud
                max_words=200).generate(title_words) 
  
# plot the WordCloud image                        
plt.figure(figsize = (10, 10), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 

#savefig will save the figure (at resolution 300dpi - good enoough for print)
plt.savefig("Covidportaltitles_tryinchyphens.png", dpi=300) 