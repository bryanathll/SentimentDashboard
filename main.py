import os
from flask import Flask, request, render_template
import numpy as np
import pandas as pd 
from  google_play_scraper import Sort, reviews
from transformers import pipeline

app = Flask(__name__)
@app.route("/", method=["GET" "POST"])
def index():
    if request.method == "POST":
        package_name = request.form["package_name"]
        result, continuation_token = reviews(
            package_name,
            lang='id',
            country='id',
            count=100,
            filter_score_with=None,
            sort=Sort.NEWEST
        )
        df = pd.DataFrame(np.array(result), columns=['review'])

        df=df.join(pd.DataFrame(df.pop('review').tolist))

        df.rename(columns={'UserName':'Username', 'content':'Review',
                'score':'Rating', 'userImage':'User Image'},inplace=True)

        df[['User Image', 'Username', 'Review', 'Raring']]

        df['User Image'] = df['User Image'].apply(
        lambda x: f'<img src="{x}" width="50" height="50">')
    
        table_classes = 'table table-responsive table-stripped'

        df_html = df.to_html(index=False, escape=False, classes=table_classes)

        return render_template('index.html', table=df_html, package_name=package_name)
    
    else:
        return render_template('index.html')

if __name__ =="__main__":
    app.run()