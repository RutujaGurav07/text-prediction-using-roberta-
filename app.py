import flask
from flask import Flask, request, render_template
import json

from matplotlib.pyplot import title
import main

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route("/login")
def login():
    return render_template('login.html' )

@app.route("/predict")
def main_prediction():
    return render_template('index.html' )

@app.route("/home")
def home():
    return render_template('home.html' )

@app.route("/about")
def about():
    return render_template('about.html' )

@app.route("/file")
def file():
    return render_template('file.html' )

@app.route("/contact")
def contact():
    return render_template('contact.html' )


@app.route('/get_end_predictions', methods=['post'])
def get_prediction_eos():
    try:
        input_text = ' '.join(request.json['input_text'].split())
        input_text += ' <mask>'
        top_k = request.json['top_k']
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(host = "localhost", debug=True, port=9000, use_reloader=False)
    