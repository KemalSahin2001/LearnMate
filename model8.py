import CEFRpredictator
from functions import generate_unknown_words
from functions import prepocess as pre
from functions import extractKW as kw
from functions import preProcessParagraphs
from functions import Labeling
import warnings 
import os
import json
warnings.filterwarnings("ignore")

def process_text_file(file_path, file_name):
    print(f"Processing: {file_name}")
    
    paragraphs, text = pre.prepocess(file_path)  
    keyword_dict= kw.extract(paragraphs, text)
    output_list = []

    for keywords, paragraph in keyword_dict.items():
        paragraph = paragraph.replace('\n', ' ')
        paragraph = paragraph.strip()

        cefr_level = CEFRpredictator.predict(paragraph)
        #unknown_words = generate_unknown_words.top_5_words(paragraph)
        #buttons = preProcessParagraphs.process_text(paragraph)
        label = Labeling.label(paragraph)

        paragraph_data = {
            "photoUrl": "to be replaced",
            "Book Name": file_name,
            "Keywords": keywords,
            #"Words you probably do not know": ', '.join(unknown_words),
            "CEFR level": cefr_level,
            "Label": label,
            #"Buttons": buttons
            "Paragraph": paragraph
        }

        output_list.append(paragraph_data)

    return output_list


folder_path = "gutenberg"
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        file_name, file_extension = os.path.splitext(filename)

        output_list = process_text_file(file_path, file_name)

        with open(f"{file_name}.json", 'w') as json_file:
            json.dump(output_list, json_file, indent=4)
