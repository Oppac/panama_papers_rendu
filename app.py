#!/usr/bin/python2
# -*- coding: utf-8 -*-
from __future__ import division
from flask import Flask, json, render_template, request
from neo4j.v1 import GraphDatabase, basic_auth
import json
import csv
import os
import time
import math
from random import randint

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("accueil.html")

@app.route("/canvasjs.min.js")
def canvasjs():
    return app.send_static_file("canvasjs.min.js")

@app.route("/accueil.js")
def accueiljs():
    return app.send_static_file("accueil.js")

@app.route("/singleAnalyse.js")
def singleAnalysejs():
    return app.send_static_file("singleAnalyse.js")

@app.route("/countries")
def country():
    op = request.args.get("country", "HKG").encode('utf8')
    t = time.time()

    with open('utils/country_id.json') as country_id_file:
    	country_id = json.load(country_id_file)

    with open('utils/country_value.json') as country_value_file:
    	country_value = json.load(country_value_file)

    with open('utils/country_relation.json') as country_relation_file:
    	country_relation = json.load(country_relation_file)

    with open('utils/country_code.json') as code_traducteur_file:
    	country_traducteur = json.load(code_traducteur_file)

    ouput_file = open('static/singleAnalyse.js', 'w')

    ouput_file.write("var analyse_cerlce_1 = [\n")
    liste_from = []
    total_from = 0
    for src in country_relation:
        if src != op and src != "None" and src != "XXX":
            if op in country_relation[src]:
                if src in country_traducteur:
                    ouput_file.write("{ y: "+str(country_relation[src][op])+", indexLabel: \""+country_traducteur[src].encode('utf8')+"\"},\n")
                else:
                    ouput_file.write("{ y: "+str(country_relation[src][op])+", indexLabel: \""+src.encode('utf8')+"\"},\n")
                total_from += country_relation[src][op]
                liste_from.append(src)
    ouput_file.write("];\n")

    ouput_file.write("var analyse_bar_1_1 = [\n")
    for i in range(len(liste_from)):
        maximum = i;
        for j in range(i+1,len(liste_from)):
            if country_relation[liste_from[j]][op] > country_relation[liste_from[maximum]][op]:
                maximum = j
        if liste_from[maximum] in country_traducteur:
            ouput_file.write("{ y: "+str(country_relation[liste_from[maximum]][op])+", label: \""+country_traducteur[liste_from[maximum]].encode('utf8')+"\"},\n")
        else:
            ouput_file.write("{ y: "+str(country_relation[liste_from[maximum]][op])+", label: \""+liste_from[maximum].encode('utf8')+"\"},\n")
        tmp = liste_from[i]
        liste_from[i] = liste_from[maximum]
        liste_from[maximum] = tmp
    ouput_file.write("];\n")

    ouput_file.write("var analyse_bar_1_2 = [\n")
    for dst in liste_from:
        if dst in country_relation[op]:
            if dst in country_traducteur:
                ouput_file.write("{ y: "+str(country_relation[op][dst])+", label: \""+country_traducteur[dst].encode('utf8')+"\"},\n")
            else:
                ouput_file.write("{ y: "+str(country_relation[op][dst])+", label: \""+dst.encode('utf8')+"\"},\n")
        else:
            if dst in country_traducteur:
                ouput_file.write("{ y: "+str(0)+", label: \""+country_traducteur[dst].encode('utf8')+"\"},\n")
            else:
                ouput_file.write("{ y: "+str(0)+", label: \""+dst.encode('utf8')+"\"},\n")
    ouput_file.write("];\n")

    ouput_file.write("var analyse_cerlce_2 = [\n")
    liste_to = []
    total_to = 0
    for dst in country_relation[op]:
        if dst != op and dst != "None" and dst != "XXX":
            if dst in country_traducteur:
                ouput_file.write("{ y: "+str(country_relation[op][dst])+", indexLabel: \""+country_traducteur[dst].encode('utf8')+"\"},\n")
            else:
                ouput_file.write("{ y: "+str(country_relation[op][dst])+", indexLabel: \""+dst.encode('utf8')+"\"},\n")
            total_to += country_relation[op][dst]
            liste_to.append(dst)
    ouput_file.write("];\n")

    ouput_file.write("var analyse_bar_2_1 = [\n")
    for i in range(len(liste_to)):
        maximum = i;
        for j in range(i+1,len(liste_to)):
            if country_relation[op][liste_to[j]] > country_relation[op][liste_to[maximum]]:
                maximum = j
        if liste_to[maximum] in country_traducteur:
            ouput_file.write("{ y: "+str(country_relation[op][liste_to[maximum]])+", label: \""+country_traducteur[liste_to[maximum]].encode('utf8')+"\"},\n")
        else:
            ouput_file.write("{ y: "+str(country_relation[op][liste_to[maximum]])+", label: \""+liste_to[maximum].encode('utf8')+"\"},\n")
        tmp = liste_to[i]
        liste_to[i] = liste_to[maximum]
        liste_to[maximum] = tmp
    ouput_file.write("];\n")

    ouput_file.write("var analyse_bar_2_2 = [\n")
    for src in liste_to:
        if src in country_relation and op in country_relation[src]:
            if src in country_traducteur:
                ouput_file.write("{ y: "+str(country_relation[src][op])+", label: \""+country_traducteur[src].encode('utf8')+"\"},\n")
            else:
                ouput_file.write("{ y: "+str(country_relation[src][op])+", label: \""+src.encode('utf8')+"\"},\n")
        else:
            if src in country_traducteur:
                ouput_file.write("{ y: "+str(0)+", label: \""+country_traducteur[src].encode('utf8')+"\"},\n")
            else:
                ouput_file.write("{ y: "+str(0)+", label: \""+src.encode('utf8')+"\"},\n")
    ouput_file.write("];\n")

    ouput_file.write("var analyse_cerlce_3 = [\n")
    if op in country_relation[op]:
        ouput_file.write("{ y: "+str(country_relation[op][op])+", indexLabel: \"Total des realtions internes\"},\n")
    else:
        ouput_file.write("{ y: "+str(0)+", label: \"Total des realtions internes\"},\n")
    ouput_file.write("{ y: "+str(total_from)+", indexLabel: \"Total des relations entrantes\"},\n")
    ouput_file.write("];\n")

    ouput_file.write("var analyse_cerlce_4 = [\n")
    if op in country_relation[op]:
        ouput_file.write("{ y: "+str(country_relation[op][op])+", indexLabel: \"Total des realtions internes\"},\n")
    else:
        ouput_file.write("{ y: "+str(0)+", label: \"Total des realtions internes\"},\n")
    ouput_file.write("{ y: "+str(total_to)+", indexLabel: \"Total des relations sortante\"},\n")
    ouput_file.write("];\n")


    ouput_file.close()

    base = ""
    if op in country_traducteur:
        base += country_traducteur[op]
    else:
        base += op
    print time.time()-t
    return render_template("singleAnalyse.html", data = base)


if __name__ == "__main__":
    app.run()
