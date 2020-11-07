from flask import Flask, render_template, request, flash, redirect, url_for
import joblib
import requests
import pandas as pd
import numpy as np
import json
from werkzeug.utils import secure_filename
import boto3
import time
# import tablib
import os
import config

# routes call
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecretkey'
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/multiplepred")
def multiplepred():
    return render_template('multiplepred.html')

@app.route("/trainmodel")
def trainmodel():
    return render_template('trainmodel.html')

@app.route("/howvegepredictorwork")
def howvegepredictorwork():
    return render_template('howvegepredictorwork.html')

@app.route("/about")
def about():
    return render_template('about.html')


# aws cloud configurations
s3 = boto3.client('s3',
                    aws_access_key_id =config.S3_KEY,
                    aws_secret_access_key =config.S3_SECRET
                     )

BUCKET_NAME = config.S3_BUCKET

# import model and single prediction
@app.route("/predict", methods=['POST'])
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
                flash("Please upload csv file and train the model" , 'error')
                return render_template('home.html')
            else:
                flash('Prediction done!' , 'success')
                return render_template('home.html', extentPrediction = extentPrediction, predictionProduction = productionPrediction)

            

# csv import for multiple prediction
@app.route('/csvimport',methods=['POST'])
def csvpredict():
    print("abc")
    if request.method == 'POST':
        img = request.files['file']
        if img:
            try:
                filename = secure_filename(img.filename)
                filename = "csv_Predict_Values.csv"
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
            except ValueError:
                flash('the file is not uploaded! Check internet connection' , 'error')
                return render_template('multiplepred.html')
            else:
                flash('The file is uploaded!' , 'success')
                return render_template('multiplepred.html')
       


# multiple prediction using csv file
@app.route("/predictcsvfile", methods=['POST'])
def predictCSVFile():
        if request.method == 'POST':
            try:
                import csvDataPrediction
                csvDataPrediction.trainModel()
                time.sleep(1)
                df = pd.read_csv("csvResult.csv")
                temp = df.to_dict('records')
                columnNames = df.columns.values 
            except ValueError:
                flash('Data not predicted!' , 'error')
                return render_template('multiplepred.html')
            else:
                # time.sleep(1)
                flash('The predicted answer was displayed! ' , 'success')
                return render_template('multiplepred.html', records=temp, colnames=columnNames)
       


# upload csv data for single prediction
@app.route('/upload',methods=['POST'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            try:
                filename = secure_filename(img.filename)
                filename = "VegetableAndClimateData.csv"
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
            except ValueError:
                flash("The file is not uploaded!" , 'error')
                return render_template('trainmodel.html')
            else:
                flash('The file is uploaded!' , 'success')
                return render_template('trainmodel.html')



# train and export the model for single prediction
@app.route("/train", methods=['POST'])
def train():
        if request.method == 'POST':
            try:
                import model
                model.trainModel()
            except ValueError:
                flash("Model is not trained. Please upload csv file and train the model!" , 'error')
                return render_template('trainmodel.html')
            else:
                flash('Model is trained!' , 'success')
                flash('Model is trained!' , 'trained')
                return render_template('trainmodel.html')

        

#Create local server and run the app in that server
if __name__ == "__main__":
    app.run()
