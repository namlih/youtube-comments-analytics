from transformers import pipeline
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import time 

app = FastAPI()
#analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
analyzer = pipeline("sentiment-analysis", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    return_all_scores=True)

summarizer = pipeline("summarization",
                      model="facebook/bart-large-cnn")


class Comment(BaseModel):
    comment: str

class Sentiment(BaseModel):
    label: str
    score: float

class SentimentList(BaseModel):
    sentimentList: List[Sentiment]

class Summary(BaseModel):
    summary: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/sentiments/")
def get_sentiment(comment: Comment):
    results = analyzer(comment.comment)[0]
    sentiments = list()
    for sentiment in results:
        sentiments.append(Sentiment(label=sentiment['label'],score=sentiment['score']))

    return SentimentList(sentimentList=sentiments)

@app.post("/summaries/")
def get_summary(comment: Comment):
    print("summarizing the comment:"+comment.comment)
    start_t = time.time()
    summary = summarizer(comment.comment, min_length=20)
    print("summarization finished in "+str(time.time()-start_t)+" seconds")
    return Summary(summary=summary[0]['summary_text'])

