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


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "Alien"))
session = driver.session()

query = "MATCH (n)-[r]->(m) where NOT r.rel_type= \"registered_address\" AND NOT r.rel_type =~ \"same*\" and NOT n.country_codes = m.country_codes WITH [n.country_codes, m.country_codes] as list return list"
table_inter = session.run(query);

couple = [" ", " "]
country_relation = {}
country_id = {}
count = 1
first = False;

for record in table_inter:
    for i in record["list"]:
        if(first):
            couple[1] = str(i)
            first = False
            for src in couple[0].split(';'):
                if src not in country_relation:
                    country_relation[src] = {}
                    country_id [src] = count
                    count += 1
                for dest in couple[1].split(';'):
                    if dest not in country_relation[src]:
                        country_relation[src][dest] = 0
                        country_id [dest] = count
                        count += 1
                    country_relation[src][dest] += 1
        else:
            couple[0] = str(i)
            first = True

query = "MATCH (n: Entity) WITH [n.country_codes] as list return list"
nb_entities = session.run(query);

country_value = {}
for record in nb_entities:
    for i in record["list"]:
        code = str(i)
        for src in code.split(';'):
            if src not in country_value:
                country_value[src] = 1
            else:
                country_value[src] +=1

session.close()


t = time.time()-t
print t


def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

def write_node(ouput_file, node_id, node_label, node_title, node_value, node_group, x, y):
    line = "{id: "+str(node_id)+",  label: '"+str(node_label)+"',  title: \""+str(node_title)+"\",  value: "+str(node_value)+", group: "+str(node_group)+", x: "+str(x)+", y: "+str(y)+", },\n"
    ouput_file.write(line)

def write_edge(ouput_file, edge_from, edge_to, edge_value):
    line = "{from: "+str(edge_from)+",  to: "+str(edge_to)+",  value: '"+str(edge_value)+"' },\n"
    ouput_file.write(line)

t = time.time()

with open('AlphaCode.json') as country_coordinates_file:
	country_coordinates = json.load(country_coordinates_file)

ouput_file = open('countries_relation.js', 'w')
ouput_file.write("var nodes = [\n")
for src in country_id:
    x, y = rotate((0,0), (country_coordinates[src][0],country_coordinates[src][1]), math.radians(-90))
    value = 0
    if src in country_value:
        value = country_value[src]
    write_node(ouput_file, country_id[src], src, src, math.sqrt(value)/10, 1, x*1000, y*1000)
ouput_file.write("];\n")

ouput_file.write("var edges = [\n")
for src in country_relation:
    for dst in country_relation[src]:
        write_edge(ouput_file, country_id[src], country_id[dst], 2)
ouput_file.write("];\n")


t = time.time()-t
print t
