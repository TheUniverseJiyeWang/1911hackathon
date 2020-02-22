#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:03:58 2019

@author: jiyewang
"""

import csv
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
#from keras.preprocessing import sequence
#from keras.models import Sequential
#from keras.layers import Dense, Dropout, Embedding, LSTM, Bidirectional
from nltk.stem.porter import PorterStemmer


stopWords = set(stopwords.words('english'))
stopWords.add('``')
stopWords.add('<')
stopWords.add('/')
stopWords.add('>')
stopWords.add('.')
stopWords.add('!')
stopWords.add("''")
stopWords.add('-')
stopWords.add('(')
stopWords.add(')')

path = 'reviews.csv'
comments = []
labels = []

with open(path,"r",encoding="utf-8",errors="ignore") as f:
    lines = csv.reader(f)
    for line in lines:
        if line[0] != None and line[0] != '':
            comments.append(line[0])
            labels.append(line[1])
            
####stem
pstm = PorterStemmer()
comments_stm = []
for comment in comments:
    splitted = comment.strip().split(' ')
    words = []
    for word in splitted:
        word = pstm.stem(word)
        words.append(word)
    comment_new = (' ').join(words)
    comments_stm.append(comment_new)
comments = comments_stm
####

####remove stop words 
comments_stpwords = []
for comment in comments:
    splitted = comment.strip().split(' ')
    words = []
    for word in splitted:
        if word not in stopWords:
            words.append(word)
    comment_new = (' ').join(words)
    comments_stpwords.append(comment_new)
comments = comments_stpwords
####
            
vectorizer =  CountVectorizer(max_features = 2500, min_df = 2, 
                              max_df = 0.8 , ngram_range = (1,1), stop_words = None, 
                              analyzer = 'word', lowercase = True)

processed_features = vectorizer.fit_transform(comments).toarray()
X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)

####Logistic Regression
print('Logistic Regression')
log_model = LogisticRegression(max_iter=200)
log_model = log_model.fit(X=X_train, y=y_train)
predictions = log_model.predict(X_test)
y_score = log_model.decision_function(X_test)
y_score = y_score[:,1]
joblib.dump(log_model,'lr_model.sav')
####

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

y_true = []

for i in y_test:
    pos = 1
    neg = 0
    if i == 'pos' or i == 1:
        y_true.append(pos)
    else:
        y_true.append(neg)

fpr,tpr,thresold = roc_curve(y_true, y_score)
auc_value = auc(fpr,tpr)
print(auc_value)

####Naive Bayes
print('Naive Bayes')
nb = GaussianNB()
nb.fit(X_train, y_train)
predictions = nb.predict(X_test)
y_score = nb.predict_proba(X_test)
y_score = y_score[:,1]
joblib.dump(nb,'nb_model.sav')
####

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

y_true = []

for i in y_test:
    pos = 1
    neg = 0
    if i == 'pos' or i == 1:
        y_true.append(pos)
    else:
        y_true.append(neg)

fpr,tpr,thresold = roc_curve(y_true, y_score)
auc_value = auc(fpr,tpr)
print(auc_value)

####SVM
print('Support Vector Machine')
svm = SVC(C=1.0, kernel = 'linear', shrinking=True, 
                probability=False, class_weight=None, 
                max_iter=-1, decision_function_shape='ovr', 
                random_state=None)
svm.fit(X_train, y_train)
predictions = svm.predict(X_test)
y_score = svm.decision_function(X_test)
y_score = y_score[:,1]
joblib.dump(svm,'svm_model.sav')
####

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

y_true = []

for i in y_test:
    pos = 1
    neg = 0
    if i == 'pos' or i == 1:
        y_true.append(pos)
    else:
        y_true.append(neg)

fpr,tpr,thresold = roc_curve(y_true, y_score)
auc_value = auc(fpr,tpr)
print(auc_value)

####RandomForest
print('Random Forest')
RFclassifier = RandomForestClassifier(n_estimators=200, random_state=0)
RFclassifier.fit(X_train, y_train)
predictions = RFclassifier.predict(X_test)
y_score = RFclassifier.predict_proba(X_test)
y_score = y_score[:,1]
joblib.dump(RFclassifier,'rf_model.sav')
####

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))
print(accuracy_score(y_test, predictions))

y_true = []

for i in y_test:
    pos = 1
    neg = 0
    if i == 'pos' or i == 1:
        y_true.append(pos)
    else:
        y_true.append(neg)

fpr,tpr,thresold = roc_curve(y_true, y_score)
auc_value = auc(fpr,tpr)
print(auc_value)



