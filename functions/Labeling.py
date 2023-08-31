from transformers import pipeline
def label(paragraph):
    classifier = pipeline("zero-shot-classification", model='cross-encoder/nli-deberta-v3-base')
    candidate_labels = categories = [
        "Science",
        "Literature",
        "Music",
        "Art",
        "History",
        "Sports",
        "Economy",
        "Cinema",
        "Psychology",
        "Environment",
        "Health",
        "Technology",
        "Fashion",
        "Food",
        "Travel",
        "Religion",
        "Politics",
        "Philosophy",
        "Business",
        "Law",
        "Sociology",
        "Physics",
        "Chemistry",
        "Biology",
        "Astronomy",
        "Engineering",
        "Architecture",
        "Mythology",
        "Astrology",
    ]
    result = classifier(paragraph, candidate_labels)
    return result['labels'][:2]