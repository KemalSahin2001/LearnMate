from pdfminer.high_level import extract_text
import re
import spacy
from nltk.stem import PorterStemmer

def extract_pdf(filename):
    text = extract_text(filename)
    return text

def read_txt(txt_path):
    with open(txt_path, "r") as txt_file:
        return txt_file.read()

def filter_gutenberg_parts(paragraphs):
    # Define regular expressions to match Gutenberg-related parts
    gutenberg_regex = r'[Gg][Uu][Tt][Ee][Nn][Bb][Ee][Rr][Gg]'

    # Remove Gutenberg-related parts from each paragraph
    filtered_paragraphs = []
    for paragraph in paragraphs:
        if not re.search(gutenberg_regex, paragraph):
            filtered_paragraphs.append(paragraph)

    return filtered_paragraphs

def foreword_split(text):
    foreword_regex = r'[Ff][Oo][Rr][Ee][Ww][Oo][Rr][Dd]'
    if re.search(foreword_regex, text) != None:
        return text.split(re.search(foreword_regex, text).group(0))[1]
    return text

def splitParagraph(paragraphs):
    i = 0
    while i < len(paragraphs):
        current_paragraph = paragraphs[i]
        current_paragraph_word_count = len(current_paragraph.split())

        if current_paragraph_word_count <= 50:
            # Check the previous paragraph
            if i > 0 and i < len(paragraphs) - 1:
                if len(paragraphs[i-1].split()) <= len(paragraphs[i+1].split()):
                    merged_paragraph = paragraphs[i-1] + "\n" + current_paragraph
                    paragraphs[i-1] = merged_paragraph
                    del paragraphs[i]
                    continue
                else:
                    merged_paragraph = current_paragraph + "\n" + paragraphs[i+1]
                    paragraphs[i+1] = merged_paragraph
                    del paragraphs[i]
                    continue
            elif i == 0:
                merged_paragraph = current_paragraph + "\n" + paragraphs[1]
                paragraphs[1] = merged_paragraph
                del paragraphs[0]
                continue
            elif i == len(paragraphs) - 1:
                merged_paragraph = paragraphs[i-1] + "\n" + current_paragraph
                paragraphs[i-1] = merged_paragraph
                del paragraphs[i]
                continue


        i += 1


def process_text(text):
    stops = ["zi", "zz"]

    #gerekli modüller
    nlp = spacy.load("en_core_web_sm")
    stemmer = PorterStemmer()
    doc = nlp(text)
    

    #irregular verbler için üç listeye ihtiyacımız var , verbs,stemmed_verbs,lemmatized verbs
    verbs = []
    stemmed_verbs = []
    lemmatized_verbs = []
    
    #verbs listesi için pos tag ile metinden verbleri çekiyoruz ve listeleri oluşturuyoruz
    for token in doc:
        if token.pos_ == 'VERB':
            verbs.append(token.text)
            stemmed_verbs.append(stemmer.stem(token.text))
            lemmatized_verbs.append(token.lemma_)

     #karşılaştırma sistemi ile irregular verb tespit ediyoruz
    irregular_verbs = []
    for x, y in zip(stemmed_verbs, lemmatized_verbs):
        if x != y:
            irregular_verbs.append(x)
    
    #irregular verbleri ayrı bir listeye aldıktan sonra normal listeden temizliyoruz
    normal_verbs = []
    for i in verbs:
        if i not in irregular_verbs:
            normal_verbs.append(i)

    #metineki şehir isimleri hariç özel isimleri silen ve geriye kalan isimleri listeye alan listeyi oluşturuyoruz
    lemmas = []
    for token in doc:
        if not token.is_punct and token.pos_ != 'VERB':
            if token.pos_ == 'PROPN':
                if token.ent_type_ == 'GPE':
                    lemmas.append(token.text.lower())
            else:
                lemmas.append(token.lemma_.lower())


    #normal fiilleri içeren listemiz normal_verbs
    #irregular verbleri içeren listemiz irregular_verbs
    #fiil harici kelimeleri içeren listemiz lemmas

    #burada da her bir fiili lemma halinde çıktı aldık           
    lemma_verbs = []
    for verb in normal_verbs:
        doc = nlp(verb)
        lemmav = doc[0].lemma_
        lemma_verbs.append(lemmav)

    

    #birleştirme ve dicte dönüştürme
    combined_dict = lemmas + lemma_verbs + irregular_verbs
           
    cleaned_list = [word for word in combined_dict if "\n" not in word]

    return cleaned_list

def prepocess(path):
    # Getting rid of the Gutenberg parts
    if path.lower().endswith(".pdf"):
        text = extract_pdf(path)
    elif path.lower().endswith(".txt"):
        text = read_txt(path)
    else:
        print("Unsupported file format.")
        return
    paragraphs = text.split("\n\n")
    splitParagraph(paragraphs)
    paragraphs = filter_gutenberg_parts(paragraphs)
    text = '\n\n'.join(paragraphs)
    text = foreword_split(text)
    paragraphs = text.split("\n\n")

    return paragraphs,text