import sys
[sys.path.append(i) for i in ['.', '..']]
from flask import Flask, request, redirect, render_template, jsonify
from flask_restx import Resource, Api

from flask_cors import CORS

import pandas as pd
import numpy as np
import pickle

from utils.retrieval import to_cat

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False ## 한글인코딩 문제로 추가함 (ascii 안 쓸거임)

CORS(app)

model = pickle.load(open('model/model.pickle', 'rb'))
with open('model/option.npy', 'rb') as f:
    opt = np.load(f, allow_pickle=True)


# @api.documentation

@app.route('/' ,methods=['GET'])
def home():
    return render_template("index.html")

@app.route('/inference', methods=['POST'])
def inference():
    # image url GET
    try:
        min_sale = int(request.form['minimum_sales_price'].strip())
        addr_dong = request.form['addr_dong'].strip()
        addr_dong = to_cat(addr_dong, opt[0])
        apartment_usage = request.form['apartment_usage'].strip()
        apartment_usage = to_cat(apartment_usage, opt[1])
        auction_count = int(request.form['auction_count'].strip())

        input_value = [addr_dong, apartment_usage, auction_count]
        df = pd.DataFrame([input_value], columns=['addr_dong', 'Apartment_usage', 'Auction_count'])
        real = model.predict(df)
        print(real)

        hammer_price = int(real * min_sale)

        result = {
            'hammer_price': format(int(hammer_price), ',')+"원",
            'addr_dong': request.form['addr_dong'].strip(),
            'apartment_usage': request.form['apartment_usage'].strip(),
            'auction_count': auction_count,
            'min_sale': format(int(min_sale), ',')+"원"
        }
    except:
        status_code = 500

    return render_template("index_result.html", params=result)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5001)