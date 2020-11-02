from flask import Flask, render_template, request
import joblib
import requests
import pandas as pd
import numpy as np
import json
from werkzeug.utils import secure_filename
import boto3
# import tablib
import os
import config



app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

s3 = boto3.client('s3',
                    aws_access_key_id =config.S3_KEY,
                    aws_secret_access_key =config.S3_SECRET,
                    # aws_session_token ="FwoGZXIvYXdzEFoaDBRAaaVEa/Dm8xFpEyKBAaiCqWcEBaHiibctBg24eUw97qJnuEPwFSaxdEvvVPkQx317qLUYZFt5AVJoajTeov15OJVIypbDoYQgJ+0H9EILryB+zU7NC1rII3C876PzEhUUk3Yeq9iI4dGAdpSQNpUu2fG7MNr5+pAexN2W9APSO9X3tzy5Ue+mQL/CQ7Cq7Sjhlv/8BTIoXj+8CXFtJytp02n8rJFbHGhEjTIAHinSHkizyojec4OuEAxTxbb8wg=="
                     )

BUCKET_NAME = config.S3_BUCKET

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
                return render_template('home.html', predictServerMsg = "Please upload csv file and train the model")

            return render_template('home.html', extentPrediction = extentPrediction, predictionProduction = productionPrediction, predictServerMsg="Prediction done")


@app.route("/train", methods=['GET', 'POST'])
def train():
        if request.method == 'POST':
            try:
                import model
            except ValueError:
                return render_template('home.html', modelTrain = "Model is not trained")
        return render_template('home.html', modelTrain = "Model is trained")


@app.route('/upload',methods=['POST'])
def upload():
    print("abc")
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
                return render_template('home.html', msg = "File not uploaded")
        return render_template('home.html', msg = "File uploaded to aws")


@app.route('/csvpredict',methods=['POST'])
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
                return render_template('home.html', msg = "File not uploaded")
        return render_template('home.html', msg = "File uploaded to aws")



@app.route("/predictCSVFile", methods=['GET', 'POST'])
def predictCSVFile():
        if request.method == 'POST':
            try:
                import csvDataPrediction
            except ValueError:
                return render_template('home.html', modelTrain = "Data not predicted")
        return render_template('home.html', modelTrain = "Data is predicted and save as csv")





@app.route("/showCSVtables", methods=['GET', 'POST'])
def show_tables():
    datasetCsv = pd.read_csv('csvResult.csv')
    df = pd.DataFrame(datasetCsv)
    data = datasetCsv
    #return dataset.html
    return render_template('home.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)
    



#Create local server and run the app in that server
if __name__ == "__main__":
    app.run()
