import os
<<<<<<< HEAD
from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd 
from  google_play_scraper import Sort, reviews
from transformers import pipeline

=======

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from google_play_scraper import Sort, reviews
from transformers import pipeline


app = Flask(__name__)

>>>>>>> 474c780 (InitialCommit)
pretrained_name = "w11wo/indonesian-roberta-base-sentiment-classifier"

nlp = pipeline(
    "sentiment-analysis",
    model=pretrained_name,
    tokenizer=pretrained_name
)

<<<<<<< HEAD
app = Flask(__name__)
=======
>>>>>>> 474c780 (InitialCommit)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        package_name = request.form["package_name"]
        result, continuation_token = reviews(
            package_name,
            lang='id',
            country='id',
            count=100,
            filter_score_with=None,
<<<<<<< HEAD
            sort=Sort.NEWEST
        )
        df = pd.DataFrame(np.array(result), columns=['review'])

        df=df.join(pd.DataFrame(df.pop('review').tolist()))

        
        df.rename(columns={'userName': 'Username', 'content': 'Review', 
                           'score': 'Rating', 'userImage': 'User Image'}, inplace=True)
        
        df = df[['User Image', 'Username', 'Review', 'Rating']]


        df['User Image'] = df['User Image'].apply
        (lambda x: f'<img src="{x}" width="50" height="50">')
    
=======
            sort=Sort.NEWEST)

        df = pd.DataFrame(np.array(result), columns=['review'])

        # Split the 'review' column into separate columns
        df = df.join(pd.DataFrame(df.pop('review').tolist()))

        # Rename columns to match HTML table headers
        df.rename(columns={'userName': 'Username', 'content': 'Review',
                  'score': 'Rating', 'userImage': 'User Image'}, inplace=True)

        # Select only the desired columns
        df = df[['User Image', 'Username', 'Review', 'Rating']]

        # Add Tailwind CSS classes to the DataFrame
        df['User Image'] = df['User Image'].apply(
            lambda x: f'<img src="{x}" width="50" height="50">')

>>>>>>> 474c780 (InitialCommit)
        table_classes = 'table table-responsive table-stripped'

        df_html = df.to_html(index=False, escape=False, classes=table_classes)

<<<<<<< HEAD
        return render_template('index.html', table=df_html, package_name=package_name)
    
    else:
        return render_template('index.html')

@app.route("/api/predict", methods='POST')
def prediction():
    if request.method == "POST":
        input_data = request.get_json()
        text = input_data['text']
        result = nlp('text')
        return jsonify({
            "status":{
                "code":200,
                "message": "Success predicting the sentiment"
            }, "data": {
                "sentiment": result}
        }),200
    else:
        return "jsonify"({
            "status":{
                "code":405,
                "message": "Method not allowed"
            },"data" : None
        }), 405

if __name__ =="__main__":
=======
        return render_template("index.html", table=df_html, package_name=package_name)

    else:
        return render_template("index.html")


@app.route("/api/hello")
def hello():
    return jsonify({
        "status": {
            "code": 200,
            "message": "Hello World!"
        },
        "data": None
    }), 200


@app.route("/api/predict", methods=["POST"])
def prediction():
    if request.method == "POST":
        input_data = request.get_json()
        texts = input_data["texts"]  # Expecting a list of texts
        results = [nlp(text) for text in texts]
        print(results)
        return jsonify({
            "status": {
                "code": 200,
                "message": "Success predicting the sentiment"
            },
            "data": {
                "sentiments": results,
            }
        }), 200

    else:
        return jsonify({
            "status": {
                "code": 405,
                "message": "Method not allowed"
            },
            "data": None
        }), 405


if __name__ == "__main__":
>>>>>>> 474c780 (InitialCommit)
    app.run()