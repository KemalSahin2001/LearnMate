import CEFRpredictator
from functions import generate_unknown_words
from functions import prepocess as pre
from functions import extractKW as kw
from functions import preProcessParagraphs
import warnings 
warnings.filterwarnings("ignore")

paragraphs,text,label = pre.prepocess("pdfs\\alchemist.pdf")
keyword_dict = kw.extract(paragraphs,text)


# Open the output file for writing-
with open('output.txt', 'w') as file:
    for keywords, paragraph in keyword_dict.items():
        paragraph = paragraph.replace('\n', ' ')
        paragraph = paragraph.strip()
        cefr_level = CEFRpredictator.predict(paragraph)
        unknown_words = generate_unknown_words.top_5_words(paragraph)
        buttons = preProcessParagraphs.process_text(paragraph)
        # Write to the file
        file.write("Keywords: " + str(keywords) + "\n")
        file.write("Words you probably do not know: " + ', '.join(unknown_words) + "\n")
        file.write("CEFR level: " + str(cefr_level) + "\n")
        file.write("Label: " + str(label) + "\n")
        file.write("Buttons: " + str(buttons) + "\n")
        file.write("-----------------------------------------------------\n")
