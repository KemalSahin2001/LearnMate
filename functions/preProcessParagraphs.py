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
    
    # Calculate the starting position of each word in the original paragraph
    word_positions = {}
    last_index = 0
    for word in words:
        word_positions[word] = paragraph.find(word, last_index)
        last_index = word_positions[word] + len(word)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    
    # Identify and remove proper nouns
    pos_tags = nltk.pos_tag(words)
    words = [word for word, pos in pos_tags if pos != 'NNP' and pos != 'NNPS']
    
    # Remove punctuation
    words = [word for word in words if word not in punctuations]
    
    # Return the processed words and their positions
    return [(word, word_positions[word]) for word in words]