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

query = "MATCH (n)-[r]->(m) where NOT r.rel_type= \"registered_address\" AND NOT r.rel_type =~ \"same*\" AND NOT r.rel_type =~ \"similare*\" WITH [n.country_codes, m.country_codes] as list return list"
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
            if src not in country_id:
                country_id[src] = count
                count += 1
            if src not in country_value:
                country_value[src] = 1
            else:
                country_value[src] +=1

session.close()

with open('utils/country_relation.json', 'w') as outfile:
    json.dump(country_relation, outfile)

with open('utils/country_id.json', 'w') as outfile:
    json.dump(country_id, outfile)

with open('utils/country_value.json', 'w') as outfile:
    json.dump(country_value, outfile)

t = time.time()-t
print t
