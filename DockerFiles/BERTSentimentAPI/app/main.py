from fastapi import FastAPI
from pydantic import BaseModel
from app.model import predict_sentiment

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(input: TextInput):
    return predict_sentiment(input.text)