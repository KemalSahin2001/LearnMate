from nltk.corpus import stopwords
import re
import unicodedata
import spacy

nlp = spacy.load('en_core_web_lg')

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
        word_positions.append((word, start_position))
        last_index = start_position + len(word)
    
    # Process the paragraph with spacy
    doc = nlp(paragraph.lower())
    
    # Create a set of proper nouns for efficient look-up
    proper_nouns = set(tok.text for tok in doc if tok.pos_ == 'PROPN')

    # Filter out proper nouns from word_positions
    word_positions = [(word, start) for word, start in word_positions if word not in proper_nouns]

    # Remove punctuation
    word_positions = [(word, start) for word, start in word_positions if word not in punctuations]

    return word_positions
