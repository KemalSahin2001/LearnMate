## Reading Scores and CEFR Level
from cefr_predictor.inference import Model
model = Model("cefr_predictor\\models\\xgboost.joblib")

def predict(texts):
    preds, probas = model.predict_decode([texts])
    response = []
    for text, pred, proba in zip([texts], preds, probas):
        row = {"text": text, "level": pred, "scores": proba}
        response.append(row)
    # Access the first (and only) item in the list, then the 'scores' dictionary
    scores = response[0]['scores']
    # Get the level with the maximum score
    max_level = max(scores, key=scores.get)    
    return max_level




