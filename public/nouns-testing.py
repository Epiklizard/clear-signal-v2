import nltk
import json
from collections import Counter
import re

# Make sure to download the required resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

sentences = []
with open("data/tech/2024-01/day_9.json", 'r') as f:
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
# Identify sentences that include frequent nouns and print them with frequency
print("\nSentences containing frequent nouns:")
for noun, freq in most_common_nouns:
    if freq >= threshold:
        # matched_sentences = []
        # for sentence in sentences:
        #     if noun in sentence:
        #         matched_sentences.append(sentence)

        print(f"Noun: '{noun}', Freq: {freq}")