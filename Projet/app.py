import requests
from flask import Flask, request, render_template, url_for
import json
import pymysql
from pymysql.cursors import DictCursor
#import pandas as pd

app = Flask(__name__)

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
    if request.method == 'POST':
        pseudo=request.form["pseudo"]
        password=request.form["password"]
        connection = pymysql.connect(host='127.0.0.1', user='root', password='root', database='projet_bootcamp', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                user= cursor.execute('SELECT * FROM users WHERE Pseudo = ?', (pseudo,)).fetchone()
                if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        finally:
            connection.close()
        return render_template(reponse)


if __name__ == '__main__':
    app.run(debug=True)



