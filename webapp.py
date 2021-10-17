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





# Load model and vectorizer
model = pickle.load(open('./models/model2.pkl', 'rb'))
TF_IDFvector = pickle.load(open('./models/tfidfvect2.pkl', 'rb'))
ps = PorterStemmer()

# def check(text):
    # review = re.sub('[^a-zA-Z]', ' ', text)
    # review = review.lower()
    # review = review.split()
    # review = [ps.stem(word) for word in review if not word in stopwords.words('english')]
    # review = ' '.join(review)
    # review_vect = TF_IDFvector.transform([review]).toarray()
    # if model.predict(review_vect) == 0:
    #     information_check = 'False'     
    # else: 
    #     information_check = 'True'
    # return information_check



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

# @app.route('/', methods=['POST'])
# def webapp():
#     # text = request.form['text']
#     # information_check = predict(text)
#     # return render_template('index.html', text=text, result=information_check)
#     return render_template('index.html')

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
    # test = model.predict(url_info_vect)
    # print("%d" % test)
    if model.predict(url_info_vect) == 0:
        information_check = False
        print(False)
    else:
        information_check = True
        print(True)
    return render_template('checkURL.html', text=url, result=information_check)
    # prediction = predict(text)
    # return render_template('checkURL.html', text=url,result=prediction)

@app.route('/checkText',methods=['GET'])
def init_checkText():
    return render_template('checkText.html')

@app.route('/checkText',methods=['POST'])
def checkText():
    text = request.form['text']
    prediction = predict(text)
    return render_template('checkText.html', text=text,result=prediction)




@app.route('/readsmart',methods=['GET'])
def readsmart():
    return render_template('readsmart.html')

if __name__ == "__main__":
    app.run()

    






'''
url = 'http://web.mta.info/developers/turnstile.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, “html.parser”)
st.button('Hit me')
st.checkbox('Check me out')
st.radio('Radio', [1,2,3])
st.selectbox('Select', [1,2,3])
st.multiselect('Multiselect', [1,2,3])
st.slider('Slide me', min_value=0, max_value=10)
st.select_slider('Slide to select', options=[1,'2'])
st.text_input('Enter some text')
st.number_input('Enter a number')
st.text_area('Area for textual entry')
st.date_input('Date input')
st.time_input('Time entry')
st.file_uploader('File uploader')
st.color_picker('Pick a color')
'''