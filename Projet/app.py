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
    return render_template("register.html")

@app.route('/new_entry', methods=['POST', 'GET'])
def connect():
    if request.method == 'POST':
        Title=str(request.form["Titre"])
        item = 0 
        while item < len(Title):
            if Title[item] == " ":
                Title.replace(" ","+")
            item += 1
        res=requests.get('http://www.omdbapi.com/?apikey=27de6cde&t=%s'%(Title))
        json_item = json.loads(res.text)
        #for item in json_item:
        titre = json_item["Title"]
        Genre = json_item["Genre"]
        score = str(json_item["Metascore"])
        print(titre,"\n",Genre,"\n",score)
        connection = pymysql.connect(host='127.0.0.1', user='root', password='root', database='projet_bootcamp', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql="insert into movies(Titre, genre, score) values(%s,%s,%s)"
                cursor.execute(sql, (titre, Genre, score))
                connection.commit()
        finally:
            connection.close()
        
        return render_template("reponse.html", reponse=json_item)

@app.route('/connect',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pseudo=request.form["pseudo"]
        password=request.form["password"]
        connection = pymysql.connect(host='127.0.0.1', user='root', password='root', database='projet_bootcamp', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                log="SELECT * FROM users WHERE Pseudo=%s AND mot_de_passe = %s"
                log2=cursor.execute(log, (pseudo, password))
                connection.commit()
                #print(log2)
                if log2 == 0:
                    error = 'Incorrect login.'
                    reponse = "form.html"
                else:
                    error = 'login succesful'
                    reponse = "home.html"
        finally:
            connection.close()
    return render_template(reponse, error=error)

@app.route('/register',methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        pseudo=request.form["pseudo"]
        password=request.form["password"]
        connection = pymysql.connect(host='127.0.0.1', user='root', password='root', database='projet_bootcamp', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                log="SELECT * FROM users WHERE Pseudo=%s"
                log2=cursor.execute(log, (pseudo))
                connection.commit()
                print(log2)
                if log2 == 1:
                    error = 'pseudo deja pris.'
                    reponse = "register.html"
                else:
                    error = 'new account created'
                    reponse = "home.html"
                    log3="insert into users (pseudo, mot_de_passe) values(%s,%s)"
                    cursor.execute(log3, (pseudo, password))
                    connection.commit()
        finally:
            connection.close()
    return render_template(reponse, error=error)


if __name__ == '__main__':
    app.run(debug=True)



