from flask import Flask, render_template, request
import joblib
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)

mul_reg_extent = open("multipleRegression_Extent_Model.pkl", "rb")
ml_model_extent = joblib.load(mul_reg_extent)

mul_reg_production = open("multipleRegression_Production_Model.pkl", "rb")
ml_model_production = joblib.load(mul_reg_production)

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/predict", methods=['GET', 'POST'])
def predict():

    print("I was here 1")
    if request.method == 'POST':


            Rainfall = float(request.form['Rainfall'])
            MaximumTemperature = float(request.form['MaximumTemperature'])
            MinimumTemperature = float(request.form['MinimumTemperature'])
            RelativeHumidity = float(request.form['RelativeHumidity'])
            Pressure = float(request.form['Pressure'])

            pred_args = [Rainfall,MaximumTemperature,MinimumTemperature,RelativeHumidity,Pressure]
            pred_args_arr = np.array(pred_args)
            pred_args_arr = pred_args_arr.reshape(1, -1)

            # For extent
            model_prediction_extent = ml_model_extent.predict(pred_args_arr)
            model_prediction_extent = round(float(model_prediction_extent), 2)

            # For Production
            model_prediction_production = ml_model_production.predict(pred_args_arr)
            model_prediction_production = round(float(model_prediction_production), 2)


    return render_template('predict.html', predictionExtent = model_prediction_extent,predictionProduction = model_prediction_production)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
