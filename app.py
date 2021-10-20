# -*- coding: utf-8 -*-

import sys
import numpy as np
from flask import Flask, request, render_template
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__, template_folder='templates', static_url_path='/static')

model = pickle.load(open('XGBoost_classification_model2.pkl', 'rb'))


@app.route('/')
def home():
    try:

        return render_template('index.html')
    except BaseException as err:
        print(err)


@app.route('/predict', methods=['POST'])
def predict():
    location = int(request.form['location'])
    updated_at = int(request.form['updated_at'])
    ID_caller = int(request.form['ID_caller'])
    opened_time = int(request.form['opened_time'])
    Support_group = int(request.form['Support_group'])
    support_incharge = int(request.form['support_incharge'])
    category_ID = int(request.form['category_ID'])
    count_updated = int(request.form['count_updated'])
    ID_status = int(request.form['ID_status'])
    val = []

    column_name = ['category_ID', 'ID_status', 'opened_time', 'updated_at', 'Support_group', 'support_incharge',
                   'location', 'count_updated', 'ID_caller']
    val.append(category_ID)
    val.append(ID_status)
    val.append(opened_time)
    val.append(updated_at)
    val.append(Support_group)
    val.append(support_incharge)
    val.append(location)
    val.append(count_updated)
    val.append(ID_caller)

    lst = np.array([val])
    scaler = MinMaxScaler()
    scaled_arr = scaler.fit_transform(lst)
    sdf = pd.DataFrame(scaled_arr, columns=column_name)

    prediction = model.predict(sdf)
    
    if prediction == 0:
        result = "Low"
    elif prediction == 1:
        result = 'Medium'
    else:
        result = 'High'
    fin_output = result
    print(fin_output)
    return render_template('index.html', prediction_text=fin_output)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
