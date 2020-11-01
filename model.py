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

# import config

S3_BUCKET = "flask-s3-crop"
S3_KEY = os.environ.get("ASIA4YEQCWGSC23WNAFY")
S3_SECRET = os.environ.get("Z/ZeHdO8qRG5E4kWMAbxY0ryC90bt7Abahl32mMi")
S3_SESSION_TOKEN = os.environ.get("FwoGZXIvYXdzEDEaDFTxbSpUYYLH9JJ8jyKCAd4W7JcX549y3+jbq8XmKXE6adTz0Y2hApKR3SLP+ApjI3Z7h3OGZD+n1sqyaUQCybYUvgU5fQwBDg3cX+8uu6mr6RFJGW5xpmJc7v9BoXqwVCHLZeBbxU7uqIh62mFE+pgXwCIyQrf11oSLb3A120kt6OClbkZINBGQfQn04shCBvco3YT2/AUyKA71Ju57c10uvIoTeBZBG9qEqPeVzoDlphh4jSFFL2XmYaDYj5DVnwg=")



# read aws csv file
client = boto3.client('s3', aws_access_key_id=config.S3_KEY, aws_secret_access_key=config.S3_SECRET)
bucket_name = config.S3_BUCKET
object_key = 'VegetableAndClimateData.csv'
csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf8')
dataset = pd.read_csv(StringIO(csv_string))

dummies_VegetableType = pd.get_dummies(dataset.VegetableType)
dummies_Distrcit = pd.get_dummies(dataset.Distrcit)


merged_Dataset = pd.concat([dataset,dummies_VegetableType,dummies_Distrcit],axis='columns')
final_Dataset = merged_Dataset.drop(['VegetableType','Distrcit',],axis='columns')

#Assign values to X without Extent & Production columns Independent varible
X = final_Dataset.drop(['Extent','Production'],axis = 'columns')
#Assign Extent data values to y #Dependent varible
y = final_Dataset.Extent
#Assign Production values to z #Dependent varible
z = final_Dataset.Production

# Splitting the dataset into the Training set and Test set for Extent Model
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=0)

# Splitting the dataset into the Training set and Test set for Production Model
XZ_train, XZ_test, z_train, z_test = train_test_split(X,z, test_size=0.2, random_state=0)

# Fitting Regression to the Training set for Extent Model
regressionExtent = RandomForestRegressor(n_estimators=20, random_state=0)
modelExtent = regressionExtent.fit(X_train, y_train)

# Fitting Regression to the Training set for Production Model
regressorProduction = RandomForestRegressor(n_estimators=20, random_state=0)
modelProduction = regressorProduction.fit(XZ_train, z_train)

# Predicting the Test set results of Extent model
y_pred = modelExtent.predict(X_test)

# Predicting the Test set results of Production model
z_pred = modelProduction.predict(XZ_test)

# Random Forest Extent model Accurecy
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
print('Variance score: %.2f' % modelExtent.score(X_test, y_test))
print('r2_score: %.2f' % r2_score(y_test,y_pred))

#Random Forest Production model Accurecy
print('Mean Absolute Error:', metrics.mean_absolute_error(z_test,z_pred))
print('Mean Squared Error:', metrics.mean_squared_error(z_test,z_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(z_test,z_pred)))
print('Variance score: %.2f' % modelProduction.score(XZ_test, z_test))
print('r2_score: %.2f' % r2_score(z_test,z_pred))

#Predict specific value
predict_SingleValue = [490.284643,28.95,24.04,82.21,98.15,0,0,0,0,1,0,0,0,0,1]
predict_SingleValue_arr = np.array(predict_SingleValue)
# ran_data_num = ran_data_arr.reshape(1,-1)

pred_Extent = regressionExtent.predict([predict_SingleValue_arr])
pred_Production = regressorProduction.predict([predict_SingleValue_arr])

print("Done")

# Exprt the models as pickle
joblib.dump(regressionExtent, "RF_modelExtent.pkl")
joblib.dump(regressorProduction, "RF_modelProduction.pkl")