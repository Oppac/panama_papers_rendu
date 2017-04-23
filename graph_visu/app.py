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

@app.route("/trade-a.csv")
def tradeacsv():
    return app.send_static_file("trade-a.csv")

@app.route("/d3.js")
def d3js():
    return app.send_static_file("d3.js")

@app.route("/underscore.js")
def underscorejs():
    return app.send_static_file("underscore.js")

@app.route("/mapper.js")
def mapperjs():
    return app.send_static_file("mapper.js")


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
    	code_traducteur = json.load(code_traducteur_file)

    nb_interTo = 0
    nb_interFrom = 0
    list_to = {}
    list_from = {}
    for dst in country_relation[op]:
    	if dst != "XXX" and dst != "None":
    		nb_interTo += country_relation[op][dst]
    		list_to[dst] = country_relation[op][dst]
    for src in country_relation:
    	if op in country_relation[src]:
    		if src != "XXX" and src != "None":
    		    nb_interFrom += country_relation[src][op]
    		    list_from[src] = country_relation[src][op]

    ouput_file = open('static/trade-a.csv', 'w')
    ouput_file.write("year,importer1,importer2,flow1,flow2\n")
    for src in list_from:
    	if src in country_relation[op]:
    		ouput_file.write("2017,"+src.encode('utf8')+","+op+","+str(list_from[src])+","+str(country_relation[op][src])+"\n")
    	else:
    		ouput_file.write("2017,"+src.encode('utf8')+","+op+","+str(list_from[src])+",0\n")

    ouput_file.close()
    print time.time()-t
    return render_template("chord-graph.html")


if __name__ == "__main__":
    app.run()
