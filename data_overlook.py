import nltk
import json
from collections import Counter
import re
from datetime import datetime





def save_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

lis = ['business', 'entertainment', 'politics', 'science', 'tech']

# overview list of a month
overview = []
for i in range(1, 30):
    overview.append({"date": datetime(2024, 2, i).strftime('%Y-%m-%d')})

for i in range(1, 30):

    for categories in lis:
        day = 0
        with open(f"data/{categories}/2024-02/summary_sheet.json", 'r') as f:
            data = json.load(f)
          
            for x in data:
                overview[day][categories] = x['frequency']
                day += 1

save_file(overview, "monthly_overview/2024-02.json")