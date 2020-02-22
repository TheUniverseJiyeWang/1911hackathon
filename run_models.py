#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:41:21 2019

@author: jiyewang
"""

import requests
import json
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score,roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.externals import joblib
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet
from nltk.stem.porter import PorterStemmer

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
        
    def search_places_by_coordinate(self, location, radius):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'location': location,
            'radius': radius,
#            'type': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        return results
    
    def search_place_by_text(self, text):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': text,
            'key': self.apiKey        
        }
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        return results     
    
    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details
    
api = GooglePlaces('AIzaS....HHG8')

fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']

input_text = "a string of address, better be street number plus post code"

###test input#####
input_text = "1333, B3H1B9"
#####test end#####

results = api.search_place_by_text(input_text)
places = results['results']
reviews_total = []
for place in places:
    types = place['types']
    details = api.get_place_details(place['place_id'], fields)
    key = 'reviews'
    if key in details['result']:
        reviews = details['result']['reviews']
        if len(reviews) >= 3:
            reviews_data = str(reviews[0]['text'])+str(reviews[1]['text'])+str(reviews[2]['text'])
        else:
            if len(reviews) == 2:
                reviews_data = str(reviews[0]['text'])+str(reviews[1]['text'])
            else:
                reviews_data = str(reviews[0]['text'])                                    
            reviews_total.append(reviews_data)
    reviews_total_string = (' ').join(reviews_total)
    
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

comments = [reviews_total_string.lower()]

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

####Vectorizer Load and Transform the input text###


####End#######

####load models####
lr_model = joblib.load('lr_model.sav')
nb_model = joblib.load('nb_model.sav')
svm_model = joblib.load('svm_model.sav')
rf_model = joblib.load('rf_model.sav')
#####load end#####

####prediction#####
lr_result = lr_model.predict(comments)
nb_result = nb_model.predict(comments)
svm_result = svm_model.predict(comments)
rf_result = rf_model.predict(comments)
######prediction end#####

print(lr_result[0])
print(nb_result[0])
print(svm_result[0])
print(rf_result[0])
    
