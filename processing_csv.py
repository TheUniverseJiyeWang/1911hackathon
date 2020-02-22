#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:05:01 2019

@author: jiyewang
"""

import csv
import re

sell_company_path = "Licensed_Direct_Selling_Companies_in_Nova_Scotia.csv"
public_housing_path = "Public_Housing_Units_-_Nova_Scotia_Seniors.csv"
coop_commercial_path = "Nova_Scotia_Co-operatives_commercial.csv"
child_care_path = "Child_Care_Directory.csv"
data_lable_path = "data_label.csv"

data_labled = []

with open(sell_company_path,'r', newline='') as f:
    lines = csv.reader(f)
    for line in lines:
        address = line[2]
        st_number_match = re.match('\d+',address)
        if st_number_match != None and line[5] != None and line[5] != '':
            st_number = st_number_match.group()
            first_3 = line[5][0:3]
            last_3 = line[5][-4:-1]
            pos_code = str(first_3)+' '+str(last_3)
            label = "business"
            row = [st_number, pos_code, label]
            data_labled.append(row)

with open(coop_commercial_path,'r', newline='') as f:
    lines = csv.reader(f)
    for line in lines:
        address = line[3]
        st_number_match = re.match('\d+',address)
        if st_number_match != None and line[6] != None and line[6] != '':
            st_number = st_number_match.group()
            label = "business"
            row = [st_number, line[6], label]
            data_labled.append(row)
            
with open(child_care_path,'r', newline='') as f:
    lines = csv.reader(f)
    for line in lines:
        address = line[21]
        st_number_match = re.match('\d+',address)
        if st_number_match != None and line[23] != None and line[23] != '':
            st_number = st_number_match.group()
            label = "business"
            row = [st_number, line[23], label]
            data_labled.append(row)
            
with open(public_housing_path,'r', newline='') as f:
    lines = csv.reader(f)
    for line in lines:
        address = line[4]
        st_number_match = re.match('\d+',address)
        if st_number_match != None and line[6] != None and line[6] != '':
            st_number = st_number_match.group()
            label = "residential"
            row = [st_number, line[6], label]
            data_labled.append(row)
            

with open(data_lable_path,'w') as f: 
    writer=csv.writer(f)
    writer.writerow(['st_number','pos_code','label'])
    for line in data_labled:
        writer.writerow(line)