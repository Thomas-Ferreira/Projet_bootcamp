import requests
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
def home():
    res=requests('http://www.omdbapi.com/?apikey=27de6cde&t=avengers&y=2012')
    json_item = json.loads(res.text)
	#print (json_item)
	for item in json_item:
		title = "Title : " + item["Title"]
        print(title)


