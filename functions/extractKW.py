from keybert import KeyBERT
from transformers import RobertaTokenizer, RobertaModel
from keyphrase_vectorizers import KeyphraseCountVectorizer

kw_model = KeyBERT()
keybert_model = KeyBERT("roberta-base")

stop_words = [
    "a", "about", "above", "after", "again", "against", "ain", "all", "am", "an", "and", "any", 
    "are", "aren", "as", "at", "be", "because", "been", "before", "being", "below", "between", 
    "both", "but", "by", "can", "couldn", "d", "did", "didn", "do", "does", "doesn", "doing", "don", 
    "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "has", "hasn", "have", 
    "haven", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", 
    "i", "if", "in", "into", "is", "isn", "it", "itself", "just", "ll", "m", "ma", "me", "mightn", 
    "more", "most", "mustn", "my", "myself", "needn", "no", "nor", "not", "now", "o", "of", "off", 
    "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "re", 
    "s", "same", "shan", "she", "should", "shouldn", "so", "some", "such", "t", "than", "that", 
    "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "this", 
    "those", "through", "to", "too", "under", "until", "up", "ve", "very", "was", "wasn", "we", 
    "were", "weren", "what", "when", "where", "which", "while", "who", "whom", "why", "will", 
    "with", "wouldn", "y", "you", "your", "yours", "yourself", "yourselves","gutenberg","ebook",
    "author","ebooks","illustrated","manuscript","literature","book","proofreading",
    "books","illustrations","project","online","edition","title","release","rights","reserved",
    "editions","edition","chapter","chapters","contents","contents","table","contents","table",
    "proofreaders","_italic","italic","punctuation","punctuation","transcriber","pretext"
]

#Cursed words should be added.
def findRelevantParagraphs(paragraphs, keywords,text,model,stop_words,n = 10,relevant_paragraphs = []):
    for paragraph in paragraphs:
        count_keywords = 0
        for keyword in keywords:
            if keyword[0] in paragraph:
                count_keywords += 1
        if count_keywords >= 2 and paragraph not in relevant_paragraphs:
            relevant_paragraphs.append(paragraph)
    
    if(len(relevant_paragraphs) < 10):        
        keywords = model.extract_keywords(text, keyphrase_ngram_range=(1,1), diversity=0.2,top_n=n+5,stop_words=stop_words,use_maxsum=True,use_mmr=True)
        findRelevantParagraphs(paragraphs,keywords,text,model,stop_words,n+5,relevant_paragraphs)
    return relevant_paragraphs 

def extract(paragraphs,book):
    
    keywordsKeybert = kw_model.extract_keywords(book, keyphrase_ngram_range=(1,1), diversity=0.2,top_n=5,stop_words=stop_words,use_maxsum=True,use_mmr=True)
    relevant_paragraphs = findRelevantParagraphs(paragraphs,keywordsKeybert,book,kw_model,stop_words)
    relevant_paragraphs = sorted(relevant_paragraphs, key=lambda p: sum([1 for keyword in keywordsKeybert if keyword[0] in p]), reverse=True)
    

    keyword_dict = {}
    for paragraph in relevant_paragraphs:
        try:
            keywordsRoberta = keybert_model.extract_keywords(paragraph, keyphrase_ngram_range=(1, 1), stop_words=stop_words, use_maxsum=True, top_n=5, use_mmr=True, diversity=0.4,vectorizer=KeyphraseCountVectorizer())
        except:
            keywordsRoberta = kw_model.extract_keywords(paragraph, keyphrase_ngram_range=(1, 1), stop_words=stop_words, use_maxsum=True, top_n=5, use_mmr=True, diversity=0.4,vectorizer=KeyphraseCountVectorizer())
        
        keywords =  [keyword[0] for keyword in keywordsRoberta]

        keyword_dict[tuple(keywords)] = paragraph


    return keyword_dict



    