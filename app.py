<<<<<<< HEAD
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from src.utils import playstore
from src.utils.config import APP_SECRET_KEY
from transformers import pipeline

app = Flask(__name__)
app.config['SECRET_KEY']= APP_SECRET_KEY
=======
import os

import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from google_play_scraper import Sort, reviews
from transformers import pipeline


app = Flask(__name__)
>>>>>>> 817d41781a87f7ee1253f9b59526eadeed4dc09c

pretrained_name = "w11wo/indonesian-roberta-base-sentiment-classifier"

nlp = pipeline(
    "sentiment-analysis",
    model=pretrained_name,
    tokenizer=pretrained_name
)

<<<<<<< HEAD
Playstore = playstore.Playstore()

@app.route("/", methods=["GET", "POST"])
def index():
        return render_template("index.html")

@app.route("/playstore", methods=['POST','GET'])
def crawl_playstore():
    if request == 'POST':
        try:
               package_name = request.form('package_name')

               processed_result_html = playstore.crawl(package_name)
               
               if not processed_result_html:
                    flash('No result found for the specified package name.')
                    return redirect(url_for('crawl_playstore'))
               return render_template('pages/playstore.html', table=processed_result_html, package_name=package_name)

        except Exception as e:
            flash('No result found for the specified package name.')
            return redirect(url_for('crawl_playstore'))
    else:
        return render_template("pages/playstore.html")
=======

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

        table_classes = 'table table-responsive table-stripped'

        df_html = df.to_html(index=False, escape=False, classes=table_classes)

        return render_template("index.html", table=df_html, package_name=package_name)

    else:
        return render_template("index.html")
>>>>>>> 817d41781a87f7ee1253f9b59526eadeed4dc09c


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
    app.run()