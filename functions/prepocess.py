from pdfminer.high_level import extract_text
import re
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