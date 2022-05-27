#-*-coding:utf-8-*-
import warnings

warnings.filterwarnings(action='ignore')

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OrdinalEncoder

from flask import Flask, send_file, send_from_directory
from flask import render_template, request, jsonify

from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS

import pandas as pd
import numpy as np
import pickle

from utils.retrieval import to_cat

app = Flask(__name__)
api = Api(
    app=app,
    doc='/',
    title='Prediction API Docs'
)
CORS(app)

model = pickle.load(open('model/model.pickle', 'rb'))
with open('model/option.npy', 'rb') as f:
    opt = np.load(f, allow_pickle=True)


@api.documentation
def custom_ui():
    return render_template("swagger-ui.html", title=api.title, specs_url="static/swagger.json")
#swagger-ui.html

@api.route('/inference')
class Inference(Resource):
    def post(self):
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

            hammer_price = real * min_sale
            result = {
                'hammer_price': int(hammer_price)
            }

        except:
            status_code = 500

        return jsonify(result)


@api.route('/test')
class Estatetest(Resource):
    def post(self):
        try:
            csv_file = request.files['file']
            sub_file = request.files['sub']

            test = pd.read_csv(csv_file)
            sub = pd.read_csv(sub_file)

            x_test = test[['addr_dong', 'Apartment_usage', 'Auction_count']]
            x_test['addr_dong'] = test['addr_dong'].apply(lambda x: to_cat(x, opt[0]))
            x_test['Apartment_usage'] = test['Apartment_usage'].apply(lambda x: to_cat(x, opt[1]))

            x_test['real'] = model.predict(x_test)

            x_test['Minimum_sales_price'] = test['Minimum_sales_price']
            x_test['Hammer_price'] = x_test['Minimum_sales_price'] * x_test['real']

            sub['Hammer_price'] = x_test['Hammer_price']

            sub.to_csv('output/predict_sub.csv', index=False)
            status_code = 200

            response = send_file('output/predict_sub.csv',
                                 mimetype='application/octet-stream',
                                 attachment_filename='predict_sub.csv',
                                 as_attachment=True)

        except:
            status_code = 500

        return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
