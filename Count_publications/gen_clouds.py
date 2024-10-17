import os

import livewordcloud as lwc

PATH = os.environ.get('PYTHONPATH')
CODE_PATH = os.environ.get('CODE_PATH')

# titles
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_all.png'),
               lwc.gen_wordcloud(field='title',
                                 data_folder=PATH,
                                 xsize=10,
                                 shape='rectangle'))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_vr.png'),
               lwc.gen_wordcloud(field='title',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20VR.json',
                                 maxwords=100))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_kaw.png'),
               lwc.gen_wordcloud(field='title',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab.json',
                                 maxwords=100))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-titles_h2020.png'),
               lwc.gen_wordcloud(field='title',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20H2020.json',
                                 maxwords=100))

# abstracts
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_all.png'),
               lwc.gen_wordcloud(field='abstract',
                                 data_folder=PATH,
                                 xsize=10,
                                 shape='rectangle'))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_vr.png'),
               lwc.gen_wordcloud(field='abstract',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20VR.json',
                                 maxwords=100))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_kaw.png'),
               lwc.gen_wordcloud(field='abstract',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20KAW/SciLifeLab.json',
                                 maxwords=100))
lwc.write_file(os.path.join(CODE_PATH, 'output/covid-portal-abstracts_h2020.png'),
               lwc.gen_wordcloud(field='abstract',
                                 data_folder=PATH,
                                 json_path='https://publications-covid19.scilifelab.se/label/Funder%3A%20H2020.json',
                                 maxwords=100))
