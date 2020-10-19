from flask import Flask, render_template, request
import joblib
import requests
import pandas as pd
import numpy as np
import json
# import model

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
        if request.method == 'POST':
            try:
                Rainfall = float(request.form['Rainfall'])
                MaximumTemperature = float(request.form['MaximumTemperature'])
                MinimumTemperature = float(request.form['MinimumTemperature'])
                RelativeHumidity = float(request.form['RelativeHumidity'])
                Pressure = float(request.form['Pressure'])
                District = request.form['DistrictName']
                Vegetable = request.form['VegetableType']
                DistrictArr = json.loads(District)
                VegetableArr = json.loads(Vegetable)

                predArr = [Rainfall,MaximumTemperature,MinimumTemperature,RelativeHumidity,Pressure]
                pred_args = np.hstack((predArr, VegetableArr, DistrictArr))

                pred_args_arr = np.array(pred_args)
                pred_args_arr = pred_args_arr.reshape(1, -1)

                mul_reg_extent = open("RF_modelExtent.pkl", "rb")
                ml_model_extent = joblib.load(mul_reg_extent)

                mul_reg_production = open("RF_modelProduction.pkl", "rb")
                ml_model_production = joblib.load(mul_reg_production)

                # For extent
                extentPrediction = ml_model_extent.predict(pred_args_arr)
                extentPrediction = round(float(extentPrediction), 2)

                # For Production
                productionPrediction = ml_model_production.predict(pred_args_arr)
                productionPrediction = round(float(productionPrediction), 2)

            except:
                return "Please check if the values are entered correctly or not"

            return render_template('home.html', extentPrediction = extentPrediction, predictionProduction = productionPrediction)


@app.route("/train", methods=['GET', 'POST'])
def train():
        if request.method == 'POST':
            try:
                import model
            except ValueError:
                return "Please check if the values are entered correctly or not"
        return render_template('home.html', modelTrain = True)


#Create local server and run the app in that server
if __name__ == "__main__":
    app.run(host='0.0.0.0')
