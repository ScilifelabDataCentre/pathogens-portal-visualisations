"""Functions for generating wordclouds for the covid publications."""

# importing all necessary modules
import io
import os

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import numpy as np
import requests

data_folder=os.path.dirname(__file__)
def gen_wordcloud(field: str = "title", data_folder=data_folder, json_path: str = "https://publications-covid19.scilifelab.se/publications.json", xsize: int = 5, ysize: int = 5, dpi: int = 150, maxwords: int = 200, shape: str = "square") -> io.BytesIO:

    """
    Generate a wordcloud file.

    Args:
        field (str): The field to evaluate.
        data_pos (str): Path to the folder containing imgs/fonts.
        json_path (str): Path to the .json file which contains the relevant publications
        xsize (int): Size on the x axis
        ysize (int): Size on the y axis
        dpi (int): DPI of the generated image. The size in pixels is determined by x*dpi x y*dpi; default: 150*5 x 150*5 = 750 x 750.
        maxwords (int): the maximum number of words that should be included in the word cloud
        shape (str): either "square" or "rectangle". the rectangle shape requires xsize double the ysize (e.g., xsize=10, ysize=5)

    Returns:
        io.BytesIO: The image as a byte stream.

    """
    # imports the .json file given in the path. e.g.,
    # https://publications-covid19.scilifelab.se/publications.json - all publications
    # https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab.json - just scilifelab funded papers
    # resp = requests.get(json_path)
    # txt = resp.json()
    
    try:
        resp = requests.get(json_path)
        # print(json_path)
        # print(resp.json())
        resp.raise_for_status()
        txt = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")

    # normalisation at this level accesses title/abstract
    # authors requires further 'digging' in the .json
    df = pd.json_normalize(txt["publications"])
    df.replace("antibody", "antibodies", regex=True, inplace=True)

    # add whatever words you'd like to exclude
    stopwords = list(STOPWORDS) + ["None", "s", "may", "two", "P", "CI",
                                   "n", "one", "three", "Conclusion", "will",
                                   "likely", "April", "day", "days", "March",
                                   "used", "due", "v", "possible", "use",
                                   "using", "year", "week", "covid-19", "sars-cov-2", "study"]

    # pick the column you want to import words from df.columnname
    title_words = " ".join(" ".join(str(val).split()) for val in df[field])

    # set the shape of the wordcloud
    if shape == "square":
      # to make a square shaped wordcloud
      mask = np.array(Image.open(os.path.join(data_folder, "SciLifeLab_symbol_POS_square.png")))
    elif shape == "rectangle":
      # to make a rectangle shaped wordcloud
      mask = np.array(Image.open(os.path.join(data_folder, "SciLifeLab_symbol_POS_rectangle.png")))

    # COVID portal visual identity
    # add font
    font_path = os.path.join(data_folder, "IBMPlexSans-Bold.ttf")

    # give colours
    # pylint: disable=unused-argument
    def multi_color_func(word=None,
                         font_size=None,
                         position=None,
                         orientation=None,
                         font_path=None,
                         random_state=None):
        if field == "title":
            colors = [[211, 56, 41]]
        elif field == "abstract":
            colors = [[208, 7, 46]]
        else:
            colors= [[338, 73, 52], [211, 56, 41],
                  [206, 62, 50], [208, 7, 46]]
        rand = random_state.randint(0, len(colors) - 1)
        return f"hsl({colors[rand][0]}, {colors[rand][1]}%, {colors[rand][2]}%)"

    wordcloud = WordCloud(background_color="white",
                          stopwords=stopwords,
                          font_path=font_path,
                          mask=mask,
                          min_font_size=14,
                          width=mask.shape[1],
                          height=mask.shape[0],
                          # 50 threshold sufficient to exclude 'ill covid'
                          # which makes little sense as a bigram
                          collocation_threshold=50,
                          color_func=multi_color_func,
                          prefer_horizontal=1,
                          # This now includes hyphens in punctuation
                          regexp=r"\w(?:[-\w])*\w?",
                          # max word default is 200, can change
                          max_words=maxwords).generate(title_words)

    # plot the WordCloud image
    plt.figure(figsize=(xsize, ysize), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    img = io.BytesIO()

    plt.savefig(img, dpi=dpi)

    return img


def write_file(filename: str, data: io.BytesIO):
    """
    Write a byte object (e.g. an image) to a file.

    Args:
        filename (str): The filename.
        data (io.BytesIO): The data object

    """
    with open(filename, "wb") as outfile:
        outfile.write(data.getbuffer())

# Generating wordclouds 
CODE_PATH = os.environ.get('CODE_PATH')

if CODE_PATH is None:
    CODE_PATH = os.getcwd()
    os.makedirs(os.path.join(CODE_PATH, 'output'), exist_ok=True)

# titles
write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_all.png'),
               gen_wordcloud(field='title',
                                 xsize=10,
                                 shape='rectangle'))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_vr.png'),
           gen_wordcloud(field='title',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20VR.json',
                         maxwords=100))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_kaw.png'),
           gen_wordcloud(field='title',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab%20National%20COVID%20program.json',
                         maxwords=100))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_h2020.png'),
           gen_wordcloud(field='title',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20H2020.json',
                         maxwords=100))

# abstracts
write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_all.png'),
           gen_wordcloud(field='abstract',
                         xsize=10,
                         shape='rectangle'))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_vr.png'),
           gen_wordcloud(field='abstract',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20VR.json',
                         maxwords=100))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_kaw.png'),
           gen_wordcloud(field='abstract',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab%20National%20COVID%20program.json',
                         maxwords=100))
write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_h2020.png'),
           gen_wordcloud(field='abstract',
                         json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20H2020.json',
                         maxwords=100))
