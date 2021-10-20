
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 00:40:59 2020

@author: SUCHARITA
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler  
from sklearn.preprocessing import StandardScaler
from statsmodels.graphics.gofplots import qqplot
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pickle
df= pd.read_excel("D:\\ExcelR\\new project\\Incidents_service.xlsx")

# replacing junk values
df["problem_id"].replace({"?": "NA"}, inplace=True)
df['problem_id'].value_counts() # NA: 139417
df["change request"].replace({"?": "NA"}, inplace=True)
df['change request'].value_counts() # NA: 140721

# understanding categorical and numerical values
categorical = [var for var in df.columns if df[var].dtype=='O']
print('There are {} categorical variables\n'.format(len(categorical)))
print('The categorical variables are :\n\n', categorical)
df[categorical].isnull().sum() # shows no null values

for var in categorical:  # view frequency of each categorical variable type, junk values are there
    print(df[var].value_counts()) # notify(139417), problem_id(140721) have almost 98% missing values
    
for var in categorical: 
    print(df[var].value_counts()/np.float(len(df)))    


for var in categorical:  # check different unique lebels for each
    print(var, 'contains ', len(df[var].unique()), ' labels')
    
numerical = [var for var in df.columns if df[var].dtype!='O']
print('There are {} numerical variables\n'.format(len(numerical)))
print('The numerical variables are :', numerical)
df[numerical].isnull().sum()

for var in numerical:  # view frequency of each numerical variable type, junk values are there
    print(df[var].value_counts())
    
for var in numerical: 
    print(df[var].value_counts()/np.float(len(df)))    # all proportions add upto 100%


for var in numerical:  # check different unique lebels for each
    print(var, ' contains ', len(df[var].unique()), ' labels')

# encoding all categorical variables
# "ID_status" have -100, which needs to be converted into string value
df["ID_status"].replace({-100: "minus hundred"}, inplace=True)
df.ID_status.value_counts()

# creating new dataframe by dropping attributes with junk values
df= df.drop(['problem_id', 'change request', 'count_opening'],axis=1)
df.shape #(141712, 22)

# removing duplicate values
duplicate= df[df.duplicated()] 
df1= df.drop_duplicates() # there are no duplicate values
df1.shape

# label encoding categorical variables

string_new= ['ID','ID_status','ID_caller','active','type_contact','impact','notify', 'opened_time', 'created_at', 'updated_at', 'Doc_knowledge', 'confirmation_check','opened_by', 'Created_by', 'updated_by', 'location', 'category_ID', 'user_symptom',  'Support_group', 'support_incharge']
number= preprocessing.LabelEncoder()
for i in string_new:
   df[i] = number.fit_transform(df[i])


# impute outliers
Q1 = df.quantile(0.25)
Q3 =df.quantile(0.75)
IQR = Q3 - Q1
low= Q1 - 1.5*IQR
high = Q3 + 1.5*IQR
print(IQR) # gives IQR for all attributes

df["count_updated"].median() # 3
df["count_updated"].mode()
df["count_updated"].mean() # 5
df["count_reassign"].median()# 1
df["count_reassign"].mode()
df["count_reassign"].mean() # 1.1

# impute all attributes with outliers togther by creating anew dataframe and loop

df3= df.loc[:,["count_updated","count_reassign"]]
df3.describe

for col_name in df3.select_dtypes(include=np.number).columns:
    print(col_name)
    q1 = df3[col_name].quantile(0.25)
    q3 = df3[col_name].quantile(0.75)
    iqr = q3 - q1
    low = q1-1.5*iqr
    high = q3+1.5*iqr 
    print("Change the outliers with median ",df3[col_name].median())
    df3.loc[(df3[col_name] < low) | (df3[col_name] > high)] = df3[col_name].median()


df4= df.drop(["count_updated","count_reassign"], axis= 1)
df4.shape
df_new= pd.concat([df4, df3],axis= 1)

x= df_new.drop(["impact"],axis= 1)
y= df_new["impact"] # series
y= pd.DataFrame(y)
y["impact"].value_counts() # 1(medium): 134335, 2(low): 3886, 0(high): 3491
# define the min max scaler
scaler= MinMaxScaler()
d_scale= scaler.fit_transform(x) # an array is getting created 
d_scale.shape #(141712, 21)
#convert array to dataframe
d_scale= pd.DataFrame(d_scale, columns= x.columns)

# y = impact (target), x= d_scale (predictors)

from imblearn.under_sampling import NearMiss

# define the undersampling method
undersample = NearMiss(version=1, n_neighbors=3)
# transform the dataset
x_re, y_re = undersample.fit_resample(d_scale, y)
x_re = x_re.drop(['notify'], axis= 1)
y_re["impact"].value_counts().plot(kind="pie")


# use x_re and y_re for test train split
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_re, y_re, test_size=.2, random_state=42)
x_col = x_train.columns

# XGBoost feature selection====================================================================
from xgboost import XGBClassifier
xgb = XGBClassifier()
xgb.fit(x_train, y_train.values.ravel())
importance = xgb.feature_importances_
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))
# plot feature importance, same as RF
plt.bar([x for x in range(len(importance))], importance)
plt.show()
from xgboost import plot_importance
plot_importance(xgb)

#=========================================================================================================
#MODEL BUILDING
#============================================================================================================

predictor = x_train.loc[:,['category_ID','ID' ,'opened_by', 'opened_time','Created_by', 'updated_by' ,'updated_at',
 'Support_group', 'support_incharge', 'location' , 'count_updated','created_at',
 'user_symptom','ID_caller']]

pred_test= x_test.loc[:,['category_ID','ID' ,'opened_by', 'opened_time','Created_by', 'updated_by' ,'updated_at',
 'Support_group', 'support_incharge', 'location' , 'count_updated','created_at',
 'user_symptom','ID_caller']]

# Building model with XGBoost---------------------------------

xgb1 = XGBClassifier(n_estimators=2000,learning_rate=0.3)
xgb1.fit(predictor,y_train.values.ravel())
train_pred_xgb = xgb1.predict(predictor)
print(confusion_matrix(y_train, train_pred_xgb))
print(classification_report(y_train, train_pred_xgb)) # 100%
y_train= pd.DataFrame(y_train)

test_pred_xgb = xgb1.predict(pred_test)
print(confusion_matrix(y_test, test_pred_xgb ))
print(classification_report(y_test, test_pred_xgb )) # 95%

with open("C:/Users/SUCHARITA/XGBoost_classification_model.pkl", "wb") as weightsfolder:
        pickle.dump(xgb1, weightsfolder)




model = pickle.load(open('C:/Users/SUCHARITA/XGBoost_classification_model.pkl','rb'))























