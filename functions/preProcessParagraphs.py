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
    words = re.findall(r"\b\w+\b", paragraph)
    
    # Calculate the starting and ending position of each word in the original paragraph
    word_positions = []
    last_index = 0
    for word in words:
        start_position = paragraph.find(word, last_index)
        word_positions.append((word, start_position))
        last_index = start_position + len(word)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    word_positions = [(word, start) for word, start in word_positions if word.lower() not in stop_words]
    
    # Identify and remove proper nouns
    pos_tags = nltk.pos_tag([word for word, _ in word_positions])
    word_positions = [(word, start) for (word, start), (_, tag) in zip(word_positions, pos_tags) if tag not in ['NNP', 'NNPS']]
    
    # Remove punctuation
    word_positions = [(word, start) for word, start in word_positions if word not in punctuations]

    return word_positions