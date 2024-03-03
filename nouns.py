import nltk
import json
from collections import Counter
import re
from datetime import datetime

# Make sure to download the required resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def analyze_a_day(date, category):
    sentences = []
    with open(f"data/{category}/2024-02/day_{date}.json", 'r') as f:
        data = json.load(f)
        for i in data:
            sentences.append(i["snippet"])

    valid_word_pattern = re.compile(r'^[a-zA-Z]+$')

    # Tokenize and tag parts of speech
    nouns = []
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        pos_tags = nltk.pos_tag(tokens)
        
        # Filter out nouns from the POS-tagged sentences, and also check with regex pattern for a valid word
        sentence_nouns = [
            word for word, pos in pos_tags
            if pos.startswith('NN') and valid_word_pattern.match(word)
        ]
        nouns.extend(sentence_nouns)  # Add the nouns to the main list

    # Now count the frequency of each noun
    noun_freq = Counter(nouns)
    # print(noun_freq)

    # Find the most common noun(s) as elements in a list, [('Amazon', 8), ('Apple', 8), ('day', 7)]
    most_common_nouns = noun_freq.most_common()

    threshold = 5  

    for noun, freq in most_common_nouns:
        if freq >= threshold:
            matched_sentences = []
            for sentence in sentences:
                if noun in sentence:
                    matched_sentences.append(sentence)

            # always return the most frequent first, so no need to return whole list
            return [noun, freq, matched_sentences]


def save_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

lis = ['business', 'entertainment', 'politics', 'science', 'tech']

for categories in lis:
    summary = []
    for i in range(1, 30):
        chosen_day = datetime(2024, 2, i).strftime('%Y-%m-%d')
        freq_noun_list = analyze_a_day(i, categories)
        element = {
            'date': chosen_day,
            'most-common-noun': freq_noun_list[0],
            'frequency': freq_noun_list[1],
            'snippets': freq_noun_list[2]
        }
        summary.append(element)

    save_file(summary, f'data/{categories}/2024-02/summary_sheet.json')
