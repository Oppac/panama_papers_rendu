#!/usr/bin/python2
# -*- coding: utf-8 -*-
import json
import csv

input_file = open('country_code.csv', 'r')
edges_reader = csv.reader(input_file)
init_row = edges_reader.next()


ouput_file = open('country_code.json', 'w')
ouput_file.write("{\n")

for row in edges_reader:
    ouput_file.write("\""+str(row[0])+"\": \""+str(row[1])+"\",\n")

ouput_file.write("}\n")
