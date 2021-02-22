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

def gen_wordcloud(field: str = "title", data_folder='./') -> io.BytesIO:
    """
    Generate a wordcloud file.

    Args:
        field (str): The field to evaluate.
        data_pos (str): Path to the folder containing imgs/fonts.

    Returns:
        io.BytesIO: The image as a byte stream.

    """
    # imports the .json from the publications library:
    # https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab.json
    # (will give just scilifelab funded papers)
    resp = requests.get("https://publications-covid19.scilifelab.se/publications.json")
    txt = resp.json()

    # normalisation at this level accesses title/abstract
    # authors requires further 'digging' in the .json
    df = pd.json_normalize(txt["publications"])
    df.replace("antibody", "antibodies", regex=True, inplace=True)

    # add whatever words you'd like to exclude
    stopwords = list(STOPWORDS) + ["None", "s", "may", "two", "P", "CI",
                                   "n", "one", "three", "Conclusion", "will",
                                   "likely", "April", "day", "days" ,"March",
                                   "used", "due", "v", "possible", "use",
                                   "using", "year", "week",]

    # pick the column you want to import words from df.columnname
    title_words = " ".join(" ".join(str(val).split()) for val in df[field])

    # to make a square shaped wordcloud
    mask = np.array(Image.open(os.path.join(data_folder, "SciLifeLab_symbol_POS.png")))

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
        colors = [[338, 73, 52], [211, 56, 41],
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
                          max_words=200).generate(title_words)

    # plot the WordCloud image
    plt.figure(figsize=(10, 10), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    img = io.BytesIO()

    # savefig will save the figure (resolution 300dpi - good enough for print)
    plt.savefig(img, dpi=300)

    return img


def write_file(filename: str, data: io.BytesIO):
    """
    Write a byte object (e.g. an image) to a file.

    Args:
        filename (str): The filename.
        data (io.BytesIO): The data object

    """
    with open(filename, 'wb') as outfile:
        outfile.write(data.getbuffer())
