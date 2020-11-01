# Importing the libraries
import numpy as np
import pandas as pd
import joblib
import boto3
import os
from io import StringIO
from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
# from flask import Flask, render_template, request
import joblib
import requests
import json
from werkzeug.utils import secure_filename
# import config


# # read aws csv file
client = boto3.client('s3', aws_access_key_id="AKIA4YEQCWGSAZKWZFLF", aws_secret_access_key="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")
bucket_name = "flask-s3-crop"

object_key = 'VegetableAndClimateData.csv'
csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf8')
dataset = pd.read_csv(StringIO(csv_string))

dummies_VegetableType = pd.get_dummies(dataset.VegetableType)
dummies_Distrcit = pd.get_dummies(dataset.Distrcit)

merged_Dataset = pd.concat([dummies_VegetableType,dummies_Distrcit,dataset],axis='columns')
final_Dataset = merged_Dataset.drop(['VegetableType','Distrcit',],axis='columns')

#asign values to X without Extent & Production columns
X = final_Dataset.iloc[:,:-2].values
#asign Extent data values to y
y = final_Dataset.iloc[:,15].values
#asign Production values to z
z = final_Dataset.iloc[:,16].values

# # Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)
XZ_train, XZ_test, z_train, z_test = train_test_split(X,z, test_size=0.2, random_state=0)

# Fitting Regression to the Training set
regressionExtent = RandomForestRegressor(n_estimators=20, random_state=0)
modelExtent = regressionExtent.fit(X_train, y_train)

regressorProduction = RandomForestRegressor(n_estimators=20, random_state=0)
modelProduction = regressorProduction.fit(XZ_train, z_train)


#---------------- Import csv file need to predict and preiction-----------------------
# # # read aws csv file
object_key = 'KandyBeansWithoutProduction.csv'
csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf8')
dataset2 = pd.read_csv(StringIO(csv_string))

# # Importing the dataset
# dataset2 = pd.read_csv("KandyBeansWithoutProduction.csv")

# Convert catogorical data into readeble format for model
dummies_VegetableType = pd.get_dummies(dataset2.VegetableType)
dummies_Distrcit = pd.get_dummies(dataset2.Distrcit)
# Merge data set
merged_Dataset = pd.concat([dummies_VegetableType,dummies_Distrcit,dataset2],axis='columns')
# Ready data for prediction
# Drop string categorical data
final_Dataset2 = merged_Dataset.drop(['VegetableType','Distrcit','Date'],axis='columns')

# Predict from model
# Prediction of Extent
extentPrediction = modelExtent.predict(final_Dataset2)
# Round the value
ExtentPrediction = np.around(extentPrediction, 2)

# Prediction of Production 
ProductionPredict = modelProduction.predict(final_Dataset2)
# Round the value
ProductionPredict = np.around(ProductionPredict, 2)

# Add headings to predicted array
data = {'Extent_Prediction': ExtentPrediction, 'Production_Predict': ProductionPredict}
PredicteddataSetTable = pd.DataFrame(data=data)

print("PredicteddataSetTable")
print(PredicteddataSetTable)

# # Concat orginal data set with predicted data array
frames = [dataset, PredicteddataSetTable]
result = pd.concat([dataset2, PredicteddataSetTable], axis=1, sort=False)

# # Export data as CSV file
df = pd.DataFrame(result)
df.to_csv (r'csvResult.csv', index = False, header=True)