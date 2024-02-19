from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from src.utils import playstore
from src.utils.config import APP_SECRET_KEY
from transformers import pipeline

app = Flask(__name__)
app.config['SECRET_KEY'] = APP_SECRET_KEY

pretrained_name = "w11wo/indonesian-roberta-base-sentiment-classifier"

nlp = pipeline(
    "sentiment-analysis",
    model=pretrained_name,
    tokenizer=pretrained_name
)

playstore = playstore.Playstore()

@app.route("/", methods=["GET"])
def hello_api():
        return render_template("index.html")

@app.route("/playstore", methods=['POST','GET'])
def crawl_playstore():
    if request.method == 'POST':
        try:
            package_name = request.form['package_name']

            processed_result_html = playstore.crawl(package_name)
               
            if not processed_result_html:
                # handle the case when result is empty
                flash('No results found for the specified package name.')
                return redirect(url_for('crawl_playstore'))
            
            return render_template('pages/playstore.html', table=processed_result_html, package_name=package_name)

        except Exception as e:
            flash('No results found for the specified package name.')
            return redirect(url_for('crawl_playstore'))
    else:
        return render_template("pages/playstore.html")

@app.route("/api/predict", methods=["POST"])
def prediction():
    if request.method == "POST":
        input_data = request.get_json()
        texts = input_data["texts"]  # Expecting a list of texts
        results = [nlp(text) for text in texts]
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
    app.run(debug=True,
            host="0.0.0.0",
            port=8080)