import spacy
import pandas as pd

df = pd.read_csv('output.csv')

score_data = dict(zip(df['word'], df['final_score']))

nlp = spacy.load('en_core_web_lg')  # or another model, depending on your language

def tokenize(text):
    doc = nlp(text)
    return [token.text for token in doc]
    
def top_5_words(paragraph):
    words = tokenize(paragraph)  # Split the paragraph into words
    scores = []

    scores = {}

    for word in words:
        score = score_data.get(word)  # Get the score for the word
        if score is not None:  # If the word exists in your data
            scores[word] = score  # Add it to the scores dictionary with word as the key

    # Now, scores is a dictionary of word: score pairs
    sorted_scores = sorted(scores.items(), key=lambda item: item[1])

    top_5 = sorted_scores[-5:]  # Get the top 5 scores

    top_5_words = [word for word, score in top_5]  # Get the words from the top 5 scored tuples

    return top_5_words