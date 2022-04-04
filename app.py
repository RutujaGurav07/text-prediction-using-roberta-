import flask
from flask import Flask, request, render_template
import json
from flask import Response
from flask_ckeditor import CKEditor
from bs4 import BeautifulSoup

from matplotlib.pyplot import title
import main

app = Flask(__name__)
ckeditor = CKEditor(app)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route('/predict')
def main_prediction():
   
    return render_template('index.html')


@app.route("/file")
def file():

    return render_template('file.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route('/get_end_predictions', methods=['POST'])
def get_prediction_eos():
    try:
        data4 = request.get_json()
        raw = BeautifulSoup(data4).get_text()
        # print(raw)
        input_text = ' '.join(raw.split())
        input_text += ' <mask>'
        top_k=5
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        # print(res)
        # print(json.dumps(res))
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


 
if __name__ == '__main__':
    app.run(host = "localhost", debug=True, port=9000, use_reloader=True)
    
