from flask import Flask, render_template, request, jsonify
import sklearn
import nltk
nltk.download('punkt')
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import streamlit as st
import newspaper 
from newspaper import Article
import urllib 

import mysql.connector
from mysql.connector import Error

# def connect():
#     """ Connect to MySQL database """
#     conn = None
#     try:
#         conn = mysql.connector.connect(host='localhost',
#                                        database='false-info-record',
#                                        user='root',
#                                        password='')
#         if conn.is_connected():
#             print('Connected to MySQL database')
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM model")

#             row = cursor.fetchone()

#             while row is not None:
#                 print(row)
#                 row = cursor.fetchone()
#         else:   
#             print('not connected')

#     except Error as e:
#         print(e)

#     finally:
#         if conn is not None and conn.is_connected():
#             conn.close()


def incrementVote(id):
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='false-info-record',
                                       user='root',
                                       password='')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT vote FROM model WHERE id="+str(id))

            vote = int(cursor.fetchone()[0])
            vote = vote + 1

            cursor.execute("UPDATE model SET vote="+ str(vote)+" WHERE id="+str(id))
            conn.commit()
        else:   
            print('not connected')

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            conn.close()
    return True

# Load model and vectorizer
model = pickle.load(open('./models/model2.pkl', 'rb'))
TF_IDFvector = pickle.load(open('./models/tfidfvect2.pkl', 'rb'))
ps = PorterStemmer()


app = Flask(__name__, template_folder='./templates')  

sps = PorterStemmer()


# Build functionalities
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

def predict(text):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review_vect = TF_IDFvector.transform([review]).toarray()
    information_check = 'False' if model.predict(review_vect) == 0 else 'True'
    return information_check

@app.route('/checkURL',methods=['GET'])
def init_checkURL():
    return render_template('checkURL.html')

@app.route('/checkURL',methods=['POST'])
def checkURL():
    url = request.form['text']
    url = urllib.parse.unquote(url)
    article = Article(str(url))
    article.download()
    article.parse()
    article.nlp()
    url_info=article.summary
    url_info_vect = TF_IDFvector.transform([url_info]).toarray()

    if model.predict(url_info_vect) == 0:
        information_check = False
        print(False)
    else:
        information_check = True
        print(True)
    return render_template('checkURL.html', text=url, result=information_check)

@app.route('/checkText',methods=['GET'])
def init_checkText():
    return render_template('checkText.html')

@app.route('/checkText',methods=['POST'])
def checkText():
    text = request.form['text']
    prediction = predict(text)
    return render_template('checkText.html', text=text,result=prediction)

@app.route('/addvote', methods=['POST'])
def addvote():
    returnpath = request.form['type']
    model = request.form['model']
    if(model=="bert"):
        id = 0
    elif(model=="ts"):
        id = 1
    else:
        id = 2
    checkAddVote = incrementVote(id)
    return render_template(returnpath, checkAddVote=checkAddVote)


@app.route('/readsmart',methods=['GET'])
def readsmart():
    return render_template('readsmart.html')

if __name__ == "__main__":
    app.run()
    

    


