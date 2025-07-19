from transformers import pipeline

# Load model once at startup
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def predict_sentiment(text: str):
    result = sentiment_pipeline(text)[0]
    return {"label": result["label"], "score": round(result["score"], 4)}