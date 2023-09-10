from pdfminer.high_level import extract_text
import re
from nltk.stem import PorterStemmer
from pathlib import Path

def extract_pdf(filename):
    text = extract_text(filename)
    return text

def read_txt(txt_path):
    path = Path(txt_path)
    text = path.read_text()
    return text

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

def splitParagraph(paragraphs, upper_limit=250):
    iteration_count = 0
    MAX_ITERATIONS = 10  # Arbitrary number to check for potential infinite loop

    while True:
        i = 0
        merge_occurred = False
        iteration_count += 1

        if iteration_count > MAX_ITERATIONS:
            upper_limit += 50
            iteration_count = 0  # Reset iteration count

        while i < len(paragraphs):
            current_paragraph = paragraphs[i].strip()
            
            if not current_paragraph:
                i += 1
                continue

            current_paragraph_word_count = len(current_paragraph.split())

            # Split longer paragraphs
            if current_paragraph_word_count > upper_limit:
                words = current_paragraph.split()
                split_index = upper_limit // 2  # default split point
                
                # find the nearest sentence end after the default split point
                for j in range(upper_limit // 2, upper_limit):
                    if words[j][-1] in [".", "?", "!"]:
                        split_index = j + 1
                        break

                # form new paragraphs after splitting
                new_paragraph_1 = ' '.join(words[:split_index])
                new_paragraph_2 = ' '.join(words[split_index:])
                paragraphs[i] = new_paragraph_1
                paragraphs.insert(i + 1, new_paragraph_2)
                merge_occurred = True
                continue

            # Merge shorter paragraphs
            elif current_paragraph_word_count <= 50:
                # If it's the first paragraph
                if i == 0:
                    merged_paragraph = current_paragraph + " " + paragraphs[i+1]
                    paragraphs[i+1] = merged_paragraph
                    del paragraphs[i]
                    merge_occurred = True
                    continue
                # If it's the last paragraph
                elif i == len(paragraphs) - 1:
                    merged_paragraph = paragraphs[i-1] + " " + current_paragraph
                    paragraphs[i-1] = merged_paragraph
                    del paragraphs[i]
                    merge_occurred = True
                    continue
                # Otherwise
                else:
                    # Conditions to decide which paragraph to merge with
                    if current_paragraph[-1] in [":", "\"", "-", "?"]:
                        merged_paragraph = current_paragraph + " " + paragraphs[i+1]
                        paragraphs[i+1] = merged_paragraph
                        del paragraphs[i]
                        merge_occurred = True
                        continue
                    else:
                        merged_paragraph = paragraphs[i-1] + " " + current_paragraph
                        paragraphs[i-1] = merged_paragraph
                        del paragraphs[i]
                        merge_occurred = True
                        continue

            i += 1

        if not merge_occurred:
            break

    return paragraphs

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