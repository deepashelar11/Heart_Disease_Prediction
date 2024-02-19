
#==================================== Importing the dependencies ====================================
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#==================================== Data collection & processing ====================================

#loading the csv data to pandas DataFrame
heart_data = pd.read_csv('dataset/heart_disease_data.csv')

#Spliting the features & target

X = heart_data.drop(columns='target', axis=1)
Y = heart_data['target']

#Spliting the data into training data & test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

#==================================== Model Training ====================================

#Load logistic regression model into Model variable
model = LogisticRegression(solver='lbfgs', max_iter=1000)

#training the LogisticRegression model with Training Data
model.fit(X_train, Y_train)

#==================================== Model Evaluation ====================================

#Accuracy on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print(" train data accuracy", training_data_accuracy)

#Accuracy on test data
X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print(" test data accuracy", test_data_accuracy)

#==================================== Building Predective System ====================================

# Create a function for prediction
def predict_heart_disease(input_data):

    # Change the input data to the numpy array
    input_data_as_numpy_array = np.asarray(input_data)

    # Reshape the numpy array as we are predicting for only one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)

    prediction = model.predict(input_data_reshaped)
    return prediction[0]



