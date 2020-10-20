# Importing the libraries
import numpy as np
import pandas as pd



from sklearn import metrics
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# import sklearn.external.joblib as extjoblib
import joblib




import boto3


s3 = boto3.client('s3')
obj = s3.get_object(Bucket='flask-s3-crop', Key='ASIA4YEQCWGSKKYQJWEW')
dataset = pd.read_csv(obj['s3://flask-s3-crop/VegetableAndClimateData.csv'])



# client = boto3.client('s3')
# path = 's3://flask-s3-crop/VegetableAndClimateData.csv'

# dataset = pd.read_csv(path)
# Importing the dataset
# dataset = pd.read_csv("VegetableAndClimateData.csv")

dummies_VegetableType = pd.get_dummies(dataset.VegetableType)
dummies_VegetableType

dummies_Distrcit = pd.get_dummies(dataset.Distrcit)
dummies_Distrcit

merged_Dataset = pd.concat([dataset,dummies_VegetableType,dummies_Distrcit],axis='columns')

final_Dataset = merged_Dataset.drop(['VegetableType','Distrcit',],axis='columns')

#Assign values to X without Extent & Production columns
X = final_Dataset.drop(['Extent','Production'],axis = 'columns')

#Assign Extent data values to y
y = final_Dataset.Extent

#Assign Production values to z
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

#Random Forest Extent model Accurecy
# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))
# print('Variance score: %.2f' % modelExtent.score(X_test, y_test))
# print('r2_score: %.2f' % r2_score(y_test,y_pred))

#Random Forest Production model Accurecy
# print('Mean Absolute Error:', metrics.mean_absolute_error(z_test,z_pred))
# print('Mean Squared Error:', metrics.mean_squared_error(z_test,z_pred))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(z_test,z_pred)))
# print('Variance score: %.2f' % modelProduction.score(XZ_test, z_test))
# print('r2_score: %.2f' % r2_score(z_test,z_pred))

#Predict specific value
predict_SingleValue = [490.284643,28.95,24.04,82.21,98.15,0,0,0,0,1,0,0,0,0,1]
predict_SingleValue_arr = np.array(predict_SingleValue)
# ran_data_num = ran_data_arr.reshape(1,-1)

pred_Extent = regressionExtent.predict([predict_SingleValue_arr])
pred_Production = regressorProduction.predict([predict_SingleValue_arr])

print("Done")

joblib.dump(regressionExtent, "RF_modelExtent.pkl")
joblib.dump(regressorProduction, "RF_modelProduction.pkl")