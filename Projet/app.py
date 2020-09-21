import requests
from flask import Flask, render_template, url_for, request
import json

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/api')
def api():
    res=requests.get('http://www.omdbapi.com/?apikey=27de6cde&t=avengers&y=2012')
    json_item = json.loads(res.text)
    return render_template("reponse.html", reponse=json_item)


if __name__ == '__main__':
    app.run(debug=True)



