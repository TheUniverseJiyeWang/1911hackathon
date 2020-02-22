#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:17:13 2019

@author: jiyewang
"""

import requests
import json
import csv

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
    
api = GooglePlaces('AIzaSy....txHHG8')

#results = api.search_place_by_text("1333 South Park St")
#location_test = str(results['results'][0]['geometry']['location']['lat'])+','+str((results['results'][0]['geometry']['location']['lng']))
#results = api.search_places_by_coordinate(location_test, "20")

###test part######
#results = api.search_places_by_coordinate("44.6405746, -63.57821509999999", "20")
#results = api.search_place_by_text("5651 B3H1B9")
#results = api.search_place_by_text("1333 B3J2K9")
#results = api.search_place_by_text("1665 B3H3K4")
#results = api.search_place_by_text("park victoria")
#results = api.search_place_by_text("1333 South Park St")

#####test end#####

fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']

reviews_dataset = []
raw_path = 'raw.csv'
count = 0

with open(raw_path,'r', newline='') as f:
    lines = csv.reader(f)
    for line in lines:
        search_text = str(line[0])+', '+str(line[1])
        results = api.search_place_by_text(search_text)
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
                count = count+1
        reviews_total_string = (' ').join(reviews_total)
        label = line[2]
        reviews_dataset.append([reviews_total_string, label])

print(count)        
reviews_path = 'reviews.csv'

with open(reviews_path,'w') as f: 
    writer=csv.writer(f)
    writer.writerow(['reviews','label'])
    for line in reviews_dataset:
        writer.writerow(line)
        
    
        
    
