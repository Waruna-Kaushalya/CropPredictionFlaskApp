from flask import Flask, render_template, request
import joblib
import requests
import pandas as pd
import numpy as np

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
        if request.method == 'POST':
            Rainfall = float(request.form['Rainfall'])
            MaximumTemperature = float(request.form['MaximumTemperature'])
            MinimumTemperature = float(request.form['MinimumTemperature'])
            RelativeHumidity = float(request.form['RelativeHumidity'])
            Pressure = float(request.form['Pressure'])

            pred_args = [Rainfall,MaximumTemperature,MinimumTemperature,RelativeHumidity,Pressure]
            pred_args_arr = np.array(pred_args)
            pred_args_arr = pred_args_arr.reshape(1, -1)

            # Load models

            District = "badulla"
            Vegetable = "Beans"

            District = request.form['DistrictName']
            Vegetable = request.form['VegetableType']


            Extent_District_Vege = District+"_"+Vegetable+"_Extent_Model.pkl"
            Production_District_Vege = District+"_"+Vegetable+"_Production_Model.pkl"

            mul_reg_extent = open(Extent_District_Vege, "rb")
            ml_model_extent = joblib.load(mul_reg_extent)

            mul_reg_production = open(Production_District_Vege, "rb")
            ml_model_production = joblib.load(mul_reg_production)

            # For extent
            model_prediction_extent = ml_model_extent.predict(pred_args_arr)
            model_prediction_extent = round(float(model_prediction_extent), 2)

            # For Production
            model_prediction_production = ml_model_production.predict(pred_args_arr)
            model_prediction_production = round(float(model_prediction_production), 2)

        return render_template('predict.html', predictionExtent = model_prediction_extent, predictionProduction = model_prediction_production)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
