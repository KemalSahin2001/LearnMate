import CEFRpredictator
from functions import generate_unknown_words
from functions import prepocess as pre
from functions import extractKW as kw
from functions import preProcessParagraphs
import warnings 
warnings.filterwarnings("ignore")

paragraphs,text = pre.prepocess("pdfs\\TheFlyingGirl.pdf")
keyword_dict = kw.extract(paragraphs,text)




# for keywords, paragraph in keyword_dict.items():
#     cefr_level = CEFRpredictator.predict(paragraph)
#     unknown_words = generate_unknown_words.top_5_words(paragraph)
#     print("Keywords:", keywords)
#     print("Paragraph:", paragraph)
#     print("Words you probably do not know:", unknown_words)
#     print("CEFR level:", cefr_level)
#     print("-----------------------------------------------------")



# Open the output file for writing-
with open('output.txt', 'w') as file:
    for keywords, paragraph in keyword_dict.items():
        cefr_level = CEFRpredictator.predict(paragraph)
        unknown_words = generate_unknown_words.top_5_words(paragraph)
        buttons = preProcessParagraphs.process_text(paragraph)
        # Write to the file instead of printing
        file.write("Keywords: " + str(keywords) + "\n")
        file.write("Paragraph: " + str(paragraph) + "\n")
        file.write("Words you probably do not know: " + ', '.join(unknown_words) + "\n")
        file.write("CEFR level: " + str(cefr_level) + "\n")
        file.write("Buttons: " + str(buttons) + "\n")
        file.write("-----------------------------------------------------\n")
