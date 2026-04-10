"""This script produces a table showing
the most recent 10 publications in the COVID-19
publications database"""
import datetime
import json
from pathlib import Path

# get data
data_path = Path(__file__).parent / "Swedish_COVID19_publications_data.json"
with open(data_path) as f:
    data = json.load(f)

# keep 10 most recent, with date today or earlier
today = str(datetime.date.today())
pubs = [pub for pub in data["publications"] if pub["published"] <= today]
recent = sorted(pubs, key=lambda x: x["published"], reverse=True)[:10]

# collapse authors
for entry in recent:
    if len(entry["authors"]) == 1:
        entry["authors"] = entry['authors'][0]['family']
    elif len(entry["authors"]) == 2:
        entry["authors"] = f"{entry['authors'][0]['family']} and {entry['authors'][1]['family']}"
    else:
        entry["authors"] = f"{entry['authors'][0]['family']} et al."
    
output = {"publications": [{"published": entry["published"],
                            "authors": entry["authors"],
                            "title": entry["title"],
                           "doi": entry["doi"]}
                           for entry in recent]}

print(json.dumps(output))
