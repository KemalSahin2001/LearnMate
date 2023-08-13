import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import string

def process_text(paragraph):
    # Tokenize the paragraph and keep track of start index of each word
    words = word_tokenize(paragraph)
    
    # Calculate the starting position of each word in the original paragraph
    word_positions = {word: paragraph.find(word) for word in words}
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stop_words]
    
    # Identify and remove proper nouns
    pos_tags = nltk.pos_tag(words)
    words = [word for word, pos in pos_tags if pos != 'NNP' and pos != 'NNPS']
    
    # Remove punctuation
    words = [word for word in words if word not in string.punctuation and (word != '’' or word != '‘' or word != '“' or word != '”')]
    
    # Return the processed words and their positions
    return [(word, word_positions[word]) for word in words]