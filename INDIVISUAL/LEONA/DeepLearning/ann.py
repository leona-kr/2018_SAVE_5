
import numpy as np
import pandas as pd


from numpy.random import seed
seed(1)
from tensorflow import set_random_seed
set_random_seed(1)

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:13].values
Y = dataset.iloc[:, 13].values

# Encoding categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])

labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])

onehotencoder = OneHotEncoder(categorical_features = [1])
X = onehotencoder.fit_transform(X).toarray()
X = X[:, 1:]


# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout #to reduce overfitting

classifier = Sequential()
classifier.add(Dense(output_dim = 22, init = 'glorot_uniform', activation = 'relu', input_dim = 11))
classifier.add(Dropout(p = 0.3))
classifier.add(Dense(output_dim = 11, init = 'glorot_uniform', activation = 'relu'))
classifier.add(Dropout(p = 0.1))
classifier.add(Dense(output_dim = 1, init = 'glorot_uniform', activation = 'sigmoid'))
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
classifier.fit(X_train, Y_train, batch_size = 10, nb_epoch = 50)

Y_pred = classifier.predict(X_test)
Y_pred = (Y_pred > 0.5)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(Y_test, Y_pred)
accu_score = accuracy_score(Y_test, Y_pred)

print('confusion_matrix=', cm)
print('accu_score=', accu_score)

# make new prediction
"""
Predict if the customer with the following informations will leave the bank:
    
Geography: France
Credit Score: 600
Gender: Male
Age: 40
Tenure: 3
Balance: 60000
Number of Products: 2
Has Credit Card: Yes
Is Active Member: Yes
Estimated Salary: 50000
"""

new_prediction = classifier.predict(sc.transform(np.array([[ 0.0,0,600,1,40,3,60000,2,1,1,50000 ]])))
new_prediction = (new_prediction > 0.5)

print('new_prediction=', new_prediction)

