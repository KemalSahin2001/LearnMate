import CEFRpredictator
from functions import generate_unknown_words
from functions import prepocess as pre
from functions import extractKW as kw
import warnings
warnings.filterwarnings("ignore")

paragraphs,text = pre.prepocess("pdfs\\TheFlyingGirl.pdf")
keyword_dict = kw.extract(paragraphs,text)

for keywords, paragraph in keyword_dict.items():
    cefr_level = CEFRpredictator.predict(paragraph)
    unknown_words = generate_unknown_words.top_5_words(paragraph)
    print("Keywords:", keywords)
    print("Paragraph:", paragraph)
    print("Words you probably do not know:", unknown_words)
    print("CEFR level:", cefr_level)
    print("-----------------------------------------------------")