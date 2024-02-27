import requests
import csv
from datetime import datetime
import unicodedata
import pandas as pd

def remove_non_ascii(text):
    return ''.join(char for char in text if unicodedata.category(char)[0] != 'C')

def shopee(url, review_limit=100):
    shop_name = url.split('/')[-1]
    url = f'https://shopee.co.id/api/v4/shop/get_shop_detail?sort_sold_out=0&username={shop_name}'
    req = requests.get(url)
    data_shop = req.json()
    shop_id = data_shop['data']['shopid']
    user_id = data_shop['data']['userid']
    count = 0
    result = []
    while True:
        try:
            count += 1
            url = f'https://shopee.co.id/api/v4/seller_operation/get_shop_ratings?limit=6&offset={count}&shop_id={shop_id}&user_id={user_id}'
            req = requests.get(url)
            data_req = req.  son()
            if len(data_req['data']) < 6 or count >= review_limit:
                break
            for value in data_req['data']:
                data_result = {
                    'nama pengguna': remove_non_ascii(value['author_username']),
                    'produk': remove_non_ascii(value['product_items'][0]['name']),
                    'review': remove_non_ascii(value['comment']),
                    'rating': value['rating_star'],
                    'waktu transaksi': datetime.utcfromtimestamp(value['ctime']).strftime('%Y-%m-%d %H:%M')
                }
                result.append(data_result)
        except KeyError:        
            break

    df = pd.DataFrame(result)

        # Rename columns to match HTML table headers

        # Select only the desired columns
    df = df[['nama pengguna', 'produk', 'review', 'rating', 'waktu transaksi']]

    print(df)
        
    # save to csv    
    # keys = result[0].keys()
    # with open(f'shoope_rating_{shop_name}.csv', 'w', newline='', encoding='utf-8') as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(result)        



if __name__ == '__main__':    
    #silakan ganti url_shope jika ingin mengambil data review dan rating dari toko lain
    url_shop = 'https://shopee.co.id/appelhouse.store'
    shopee(url_shop, review_limit=5)