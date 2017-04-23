#!/usr/bin/python2
# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase, basic_auth
import json
import csv
import os
import time
import math
from random import randint

t = time.time()

with open('utils/country_id.json') as country_id_file:
	country_id = json.load(country_id_file)

with open('utils/country_value.json') as country_value_file:
	country_value = json.load(country_value_file)

with open('utils/country_relation.json') as country_relation_file:
	country_relation = json.load(country_relation_file)

with open('utils/country_code.json') as code_traducteur_file:
	code_traducteur = json.load(code_traducteur_file)

ouput_file = open('static/accueil.js', 'w')

nb_interIn = {}
nb_interOff = {}
for src in country_relation:
    for dst in country_relation[src]:
        if src == dst:
            nb_interIn[src] = country_relation[src][dst]
        else:
            if src not in nb_interOff:
                nb_interOff[src] = country_relation[src][dst]
            else:
                nb_interOff[src] += country_relation[src][dst]

###########################################################################

top_10_name = []
minimum = 0
c = 0
for src in country_value:
    if src != "XXX" and src != "None":
        if c == 0:
            top_10_name.append(src)
            c += 1
        elif c < 10:
            top_10_name.append(src)
            if country_value[src] < country_value[top_10_name[minimum]]:
                minimum = c
            c += 1
        else:
            if country_value[src] > country_value[top_10_name[minimum]]:
                top_10_name[minimum] = src
                for i in range(10):
                    if country_value[top_10_name[i]] < country_value[top_10_name[minimum]]:
                        minimum = i

ouput_file.write("var list_entities_1 = [\n")
c = 0
while(c < 10):
    maximum = c
    for i in range(c,10):
        if country_value[top_10_name[i]] > country_value[top_10_name[maximum]]:
            maximum = i
    if top_10_name[maximum] in code_traducteur:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+code_traducteur[top_10_name[maximum]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+top_10_name[maximum]+"\"},\n")
    tmp = top_10_name[maximum]
    top_10_name[maximum] = top_10_name[c]
    top_10_name[c] = tmp
    c += 1

ouput_file.write("];\n")

ouput_file.write("var list_entities_2 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var list_entities_3 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var donut_entities = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(country_value[top_10_name[i]])+", indexLabel: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(country_value[top_10_name[i]])+", indexLabel: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

################################################################

top_10_name = []
minimum = 0
c = 0

for src in nb_interIn:
    if src != "XXX" and src != "None":
        if c == 0:
            top_10_name.append(src)
            c += 1
        elif c < 10:
            top_10_name.append(src)
            if nb_interIn[src] < nb_interIn[top_10_name[minimum]]:
                minimum = c
            c += 1
        else:
            if nb_interIn[src] > nb_interIn[top_10_name[minimum]]:
                top_10_name[minimum] = src
                for i in range(10):
                    if nb_interIn[top_10_name[i]] < nb_interIn[top_10_name[minimum]]:
                        minimum = i


ouput_file.write("var list_interIn_1 = [\n")
c = 0
while(c < 10):
    maximum = c
    for i in range(c,10):
        if nb_interIn[top_10_name[i]] > nb_interIn[top_10_name[maximum]]:
            maximum = i
    if top_10_name[maximum] in code_traducteur:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+code_traducteur[top_10_name[maximum]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+top_10_name[maximum]+"\"},\n")
    tmp = top_10_name[maximum]
    top_10_name[maximum] = top_10_name[c]
    top_10_name[c] = tmp
    c += 1

ouput_file.write("];\n")

ouput_file.write("var list_interIn_2 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var list_interIn_3 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var donut_interIn = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", indexLabel: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", indexLabel: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

################################################################

top_10_name = []
minimum = 0
c = 0
for src in nb_interOff:
    if src != "XXX" and src != "None":
        if c == 0:
            top_10_name.append(src)
            c += 1
        elif c < 10:
            top_10_name.append(src)
            if nb_interOff[src] < nb_interOff[top_10_name[minimum]]:
                minimum = c
            c += 1
        else:
            if nb_interOff[src] > nb_interOff[top_10_name[minimum]]:
                top_10_name[minimum] = src
                for i in range(10):
                    if nb_interOff[top_10_name[i]] < nb_interOff[top_10_name[minimum]]:
                        minimum = i


ouput_file.write("var list_interOff_1 = [\n")
c = 0
while(c < 10):
    maximum = c
    for i in range(c,10):
        if nb_interOff[top_10_name[i]] > nb_interOff[top_10_name[maximum]]:
            maximum = i
    if top_10_name[maximum] in code_traducteur:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+code_traducteur[top_10_name[maximum]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(country_value[top_10_name[maximum]])+", label: \""+top_10_name[maximum]+"\"},\n")
    tmp = top_10_name[maximum]
    top_10_name[maximum] = top_10_name[c]
    top_10_name[c] = tmp
    c += 1

ouput_file.write("];\n")

ouput_file.write("var list_interOff_2 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interIn[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var list_interOff_3 = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", label: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

ouput_file.write("var donut_interOff = [\n")
for i in range(10):
    if top_10_name[i] in code_traducteur:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", indexLabel: \""+code_traducteur[top_10_name[i]]+"\"},\n")
    else:
        ouput_file.write("{ y: "+str(nb_interOff[top_10_name[i]])+", indexLabel: \""+top_10_name[i]+"\"},\n")
ouput_file.write("];\n")

#####################################################################

ouput_file.write("var country_select = {\n")
for src in country_id:
    if src in code_traducteur:
        ouput_file.write(src.encode('utf8')+": \""+code_traducteur[src].encode('utf8')+"\",\n")
    else:
        ouput_file.write(src+": \""+src.encode('utf8')+"\",\n")
ouput_file.write("};\n")

ouput_file.close()

t = time.time()-t
print t
