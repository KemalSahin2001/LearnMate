import nltk
from nltk.corpus import stopwords
import string
import re

import unicodedata

punctuations = []

for i in range(0xFFFF):  # You can increase this range if necessary
    char = chr(i)
    if unicodedata.category(char).startswith('P'):
        punctuations.append(char)

def process_text(paragraph):
    # Tokenize the paragraph without splitting contractions
    pattern = r"\b\w+(?:['’]\w+)?\b"
    words = re.findall(pattern, paragraph)
    
    # Calculate the starting and ending position of each word in the original paragraph
    word_positions = []
    last_index = 0
    for word in words:
        start_position = paragraph.find(word, last_index)
        word_positions.append((word, start_position, "button"))
        last_index = start_position + len(word)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_positions = [(word, start, "stop-word") if word.lower() in stop_words else (word, start, lbl) for word, start, lbl in word_positions]
    
    # Identify and remove proper nouns
    pos_tags = nltk.pos_tag([word for word, _, _ in word_positions])
    word_positions = [(word, start, "proper-noun") if tag in ['NNP', 'NNPS'] else (word, start, label) for (word, start, label), (_, tag) in zip(word_positions, pos_tags)]
    
    # Remove punctuation
    word_positions = [(word, start,lbl) for word, start,lbl in word_positions if word not in punctuations]

    return word_positions