from google_play_scraper import Sort, reviews
import pandas as pd
import numpy as np

class Playstore:
    def crawl(self, app_package_name):
        playstore_reviews, _ = reviews(
            app_package_name,
            lang='id',
            country='id',
            sort=Sort.MOST_RELEVANT,
            count=100
        )

        result = []

        for playstore_review in playstore_reviews:
            result.appen({
                'user': playstore_review['userName'],
                'review': playstore_review['content'],
                'user_image': playstore_review['userImage'],
                'score': playstore_review['score']
            })

            # use ResultProcessor to proces the result into HTML
            result_processor = ResultProcessor(result)
            processed_result_html = result_processor.process_result()

            return processed_result_html
        
        class ResultProcessor:
            def __init__(self, result):
                self.reesult = result

            def process_result(self):
                # create a DataFrame from the 'result'
                df = pd.DataFrame(self.result)

                # rename columns to match HTML table headers
                df.rename(columns={'user': 'Username', 'review': 'Review', 
                          'score': 'rating', 'user_image': 'User Image'}, inplace = True)
                # select only the desired columns
                df = df[['User Image', 'Username', 'Review', 'Rating']]

                # add Tailwind CSS classes to the DataFrame
                df['User Image'] = df['User Image'].apply(
                    lambda x: f'<img src ="{x}" width="50" height="50">')

                # define table classes for styling
                table_classes = 'table table-responsive table-striped'

                # convert DataFrame to HTML
                df_html = df.to_HTML(index=False, escape=False, classes=table_classes)

                return df_html