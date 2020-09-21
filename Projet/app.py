import requests
from flask import Flask, render_template, url_for, request
import json
import pymysql
from pymysql.cursors import DictCursor
import pandas as pd

app = Flask(__name__)

conf = {'db': 'projet_bootcamp',
        'port': 3306,
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'charset': 'utf8' }

@app.route('/')
def home():
	return render_template('form.html')

@app.route('/api')
def api():
    res=requests.get('http://www.omdbapi.com/?apikey=27de6cde&t=avengers&y=2012')
    json_item = json.loads(res.text)
    return render_template("reponse.html", reponse=json_item)

@app.route('/connect', methods=['POST', 'GET'])
def connect():
    pseudo=requests.get("pseudo")
    password=request.get("password")
    con= pymysql.connect(**conf)
    dictionary={}
    dictionary=con.cursor.execute('SELECT * FROM users WHERE Pseudo= %s AND mot_de_passe=%s', (pseudo,password))
    if dictionary is None:
        reponse="form.html"
    else:
        reponse="home.html"
    return render_template(reponse)

    


if __name__ == '__main__':
    app.run(debug=True)



