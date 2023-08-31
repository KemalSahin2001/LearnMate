from nltk.corpus import stopwords
import re
import unicodedata
import spacy

nlp = spacy.load('en_core_web_lg')
def is_clickable(token):
    if token.is_punct or token.is_space:
        return 0
    else:
        return 1
    
def text_to_tuples(text, pattern):
        result = []
        last_index = 0

        # Tokenize using the regex pattern to capture words, punctuation, and spaces.
        tokens = re.findall(pattern, text)

        for token in tokens:
            # Use spaCy to process each token and determine its nature
            processed_token = nlp(token)[0]
            
            start_position = text.find(token, last_index)
            result.append((token, start_position, is_clickable(processed_token)))
            last_index = start_position + len(token)

        return result
def process_text(paragraph):
    # Pattern to capture words, spaces, and punctuation
    pattern = r"\b\w+(?:['’]\w+)?\b|[\s]|[.,!?;]"

    result = text_to_tuples(paragraph, pattern)
    return result

