from flask import Flask, render_template, request, jsonify
import sklearn
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import urllib
from newspaper import Article

app = Flask(__name__, template_folder='./templates')

# Load model and vectorizer
model = pickle.load(open('./models/model_new.pkl', 'rb'))
TF_IDFvector = pickle.load(open('./models/TF-IDF_Vector_new.pkl', 'rb'))
ps = PorterStemmer()

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

def checkText(text):
    review = re.sub('[^a-zA-Z]', ' ', text)
    review = review.lower()
    review = review.split()
    review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    review = ' '.join(review)
    review_vect = TF_IDFvector.transform([review]).toarray()
    if model.predict(review_vect) == 0:
        information_check = 'False'     
    else: 
        information_check = 'True'
    return information_check


@app.route('/', methods=['POST'])
def webapp():
    text = request.form['text']
    information_check = checkText(text)
    return render_template('index.html', text=text, result=information_check)

@app.route('/checkText/', methods=['GET','POST'])
def api():
    text = request.args.get("text")
    information_check = checkText(text)
    return jsonify(information_check=information_check)

@app.route('/checkUrl/', methods=['GET','POST'])
def checkUrl():
    url=request.get_data(as_text=True)[5:]
    url = urllib.parse.unquote(url)
    article = Article(str(url))
    article.download()
    article.parse()
    article.nlp()
    url_info=article.summary
    url_info_vect = TF_IDFvector.transform([url_info]).toarray()
    if model.predict(url_info_vect) == 0:
        information_check = 'False'     
    else: 
        information_check = 'True'
    return render_template('index.html', result=information_check)

if __name__ == "__main__":
    app.run()




''' #Sreamlit

import streamlit as st

st.title("Missinformation Detection")
st.text("")
st.text("")
user_input_text = st.text_input("Enter the content: ")


type_input = st.selectbox("What type of the content you want us to evaluate?",
            ("Text Content", "URL"))
button_submit = st.button("Submit")
if(button_submit):
    if(type_input == "Text Content"):
        st.text("You have picked Text Content")
        sourceCheck = check(user_input_text)
    elif(type_input == "URL"):  
        st.text("You have picked URL")

    point = sourceCheck #sample code
    suggested_art =  ["https://www.washingtonexaminer.com", "facebook.com"]
    st.text("After evaluating, we have the following report for you: ")
    st.text("Correctness: %s" % point)
    st.text("Suggested reliable article: ")
    for x in suggested_art:
        st.write("[%s](%s)"%(x,x))
'''