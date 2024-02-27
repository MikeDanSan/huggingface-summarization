from transformers import pipeline
import urllib.request
from bs4 import BeautifulSoup
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

class SummarizeRequest(BaseModel):
    url: str


import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def extract_from_url(url):

    text = ""
    req = urllib.request.Request(
            url, data=None, 
            headers={
            'User-Agent': 'Mozilla/5.0'}
        )
    html = urllib.request.urlopen(req)
    parser = BeautifulSoup(html, 'html.parser')
    for paragraph in parser.find_all('p'):
        text += paragraph.get_text()

    return text

def process(text):
    
    sumarizer = pipeline('summarization', model='t5-base', tokenizer='t5-base', truncation=True, framework='tf')

    result = sumarizer(text, min_length=180, truncation=True)
    return result[0]['summary_text']

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    url = request.url
    text = extract_from_url(url)
    return Response(text)
    click.echo(process(text))

@app.get("/")
def root():
    return Response("<h1>Summarizer API</h1>")
