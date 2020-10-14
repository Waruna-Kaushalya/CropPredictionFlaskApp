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



            # Load models
            # District = "badulla"
            # Vegetable = "Beans"

            # V_beans = 0
            # V_beetroot = 0
            # V_carrot = 0
            # V_knohkhol = 0
            # V_leeks = 0
            # D_badulla = 0
            # D_kandy = 0
            # D_matale = 0
            # D_nuwaraeliya = 0
            # D_ratnapura = 0



            # if  District == "badulla":
            #     D_badulla = 1
            # elif District == "kandy":
            #     D_kandy = 1
            # elif District == "matale":
            #     D_matale = 1
            # elif District == "nuwaraeliya":
            #     D_nuwaraeliya = 1
            # else:
            #     D_ratnapura = 1
            #
            #
            # if  Vegetable == "beans":
            #     V_beans = 1
            # elif  Vegetable == "beetroot":
            #     V_beetroot = 1
            # elif  Vegetable == "carrot":
            #     V_carrot = 1
            # elif  Vegetable == "knohkhol":
            #     V_knohkhol = 1
            # else:
            #     V_leeks = 1


            import json


            District = request.form['DistrictName']
            Vegetable = request.form['VegetableType']


            DistrictArr = json.loads(District)
            VegetableArr = json.loads(Vegetable)

            print("__________________________________________")
            print(DistrictArr[0])
            print(VegetableArr[0])
            print("__________________________________________")


            # import numpy as np
            # arr = np.hstack((arr1, arr2))

            # pred_args = [Rainfall,MaximumTemperature,MinimumTemperature,RelativeHumidity,Pressure,V_beans,V_beetroot,V_carrot,V_knohkhol,V_leeks,D_badulla,D_kandy,D_matale,D_nuwaraeliya,D_ratnapura]
            predArr = [Rainfall,MaximumTemperature,MinimumTemperature,RelativeHumidity,Pressure]

            # pred_args = np.hstack((predArr + DistrictArr + VegetableArr))
            pred_args = predArr + VegetableArr + DistrictArr

            print("+++++++++++++++++++++++++++++++++++++++++")
            print(pred_args)
            print("++++++++++++++++++++++++++++++++++++++++++")

            pred_args_arr = np.array(pred_args)
            pred_args_arr = pred_args_arr.reshape(1, -1)


            # Extent_District_Vege = District+"_"+Vegetable+"_Extent_Model.pkl"
            # Production_District_Vege = District+"_"+Vegetable+"_Production_Model.pkl"

            mul_reg_extent = open("RF_modelExtent.pkl", "rb")
            ml_model_extent = joblib.load(mul_reg_extent)

            mul_reg_production = open("RF_modelProduction.pkl", "rb")
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
