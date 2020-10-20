from flask import Flask, render_template, request
import joblib
import requests
import pandas as pd
import numpy as np
import json

from werkzeug.utils import secure_filename
import boto3

# import model


app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

s3 = boto3.client('s3',
                    aws_access_key_id="ASIA4YEQCWGSKKYQJWEW",
                    aws_secret_access_key= "tY1etzKZCuVBbBZ3V0zpp1RT62allC4WGm62KWta",
                    aws_session_token="FwoGZXIvYXdzEB0aDLnjOxpwwXlJkWP93CKCAVArCdLWk1/cj1BWlSYExRQPJdmuksPFMUrU8NlUZJJqmlquk/otQ1Y211NrtNmSiapGS1CzFaD5/x//dUFWKXveM7VZrVJ+FkDe9y35mjWw1vsf3NGCmqA/yIwcffVrxGMPOJIyRvPQI1Pf3DK9/jCx0ouaD+wmdr0uue2GdoZE7zgoubm5/AUyKMwuGqjDPa6TjQy9fLYd4tb19urTseLp+slK+0F/2LevicZOXbdu7y0="
                     )


BUCKET_NAME='flask-s3-crop'







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
                return render_template('home.html', modelTrain = "err")
        return render_template('home.html', modelTrain = "Model is trained")


@app.route('/upload',methods=['POST'])

def upload():
    print("abc")
    if request.method == 'POST':
        img = request.files['file']
        msg = "nt ! "
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
                return render_template('home.html', msg = "File uploaded to AWS")

    return render_template('home.html', msg = "File uploaded to AWS")


#Create local server and run the app in that server
if __name__ == "__main__":
    app.run()
