#--------------------Importing Required Libraries/Modules-----------------------#
import numpy as np
import pandas as pd

# Load dataset
dataset = pd.read_csv("roo_data.csv")

#---------Testing by displaying whether data is loaded properly or not-----------#
data = dataset.iloc[:,:-1].values
label = dataset.iloc[:,-1].values
len(data[0])

#--------------- Label Encoding -----------#
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

labelencoder = LabelEncoder()

#--------------- Conversion of all categorical column values to vector/numerical --------#
for i in range(14, 38):
    data[:, i] = labelencoder.fit_transform(data[:, i])

#-------------- Normalizing the non-categorical column values ---------#
from sklearn.preprocessing import Normalizer

data1 = data[:, :14]
normalized_data = Normalizer().fit_transform(data1)

data2 = data[:, 14:]
df1 = np.append(normalized_data, data2, axis=1)

#-------------------------- Adding Headers -----------------------#
X1 = pd.DataFrame(df1, columns=['Acedamic percentage in Operating Systems', 'percentage in Algorithms',
    'Percentage in Programming Concepts', 'Percentage in Software Engineering', 'Percentage in Computer Networks',
    'Percentage in Electronics Subjects', 'Percentage in Computer Architecture', 'Percentage in Mathematics',
    'Percentage in Communication skills', 'Hours working per day', 'Logical quotient rating', 'hackathons',
    'coding skills rating', 'public speaking points', 'can work long time before system?', 'self-learning capability?',
    'Extra-courses did', 'certifications', 'workshops', 'talenttests taken?', 'olympiads', 'reading and writing skills',
    'memory capability score', 'Interested subjects', 'interested career area ', 'Job/Higher Studies?', 'Type of company want to settle in?',
    'Taken inputs from seniors or elders', 'interested in games', 'Interested Type of Books', 'Salary Range Expected',
    'In a Relationship?', 'Gentle or Tuff behaviour?', 'Management or Technical', 'Salary/work', 'hard/smart worker',
    'worked in teams ever?', 'Introvert'])

#------------------ Encoding Final Output column Values ------------#
label = labelencoder.fit_transform(label)
y = pd.DataFrame(label, columns=["Suggested Job Role"])

#------------------ Training and Testing with Decision Tree ----------------#
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.2, random_state=10)

#----------------- Decision Tree -----------------------#
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
from sklearn.metrics import confusion_matrix

y_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

print("Confusion matrix:", cm)
print("Accuracy:", accuracy * 100)

#--------------- SVM ------------------------#
from sklearn import svm

svc_clf = svm.SVC()
svc_clf.fit(X_train, y_train)
svm_y_pred = svc_clf.predict(X_test)

svm_cm = confusion_matrix(y_test, svm_y_pred)
svm_accuracy = accuracy_score(y_test, svm_y_pred)

print("SVM Confusion matrix:", svm_cm)
print("SVM Accuracy:", svm_accuracy * 100)

#------------------ XGBoost --------------#
X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.3, random_state=10)
X_train.shape

#------------ Converting values of training and testing data into int64 datatype -------#
X_train = pd.to_numeric(X_train.values.flatten())
X_train = X_train.reshape((X_train.shape[0] // 38, 38))

#------------- Importing and defining XGBoost functions -----#
from xgboost import XGBClassifier

model = XGBClassifier()
#----------- Training and testing with XGBoost ------#
model.fit(X_train, y_train)
xgb_y_pred = model.predict(X_test)

xgb_cm = confusion_matrix(y_test, xgb_y_pred)
xgb_accuracy = accuracy_score(y_test, xgb_y_pred)

print("XGBoost Confusion matrix:", xgb_cm)
print("XGBoost Accuracy:", xgb_accuracy * 100)

#------------------- Saving the Model ------------------------#
import os
import pickle

if not os.path.exists('./newmodels'):  # create models directory if it doesn't exist
    os.mkdir('newmodels')

# Save Models
pickle.dump(svc_clf, open('newmodels/svc_model.h5', 'wb'))  # SVC Model
pickle.dump(clf, open('newmodels/decision_tree_model.h5', 'wb'))  # Decision Tree Model
pickle.dump(model, open('newmodels/xgb_model.h5', 'wb'))  # XGBoost Model
