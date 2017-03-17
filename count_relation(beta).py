#!/usr/bin/python2
# -*- coding: utf-8 -*-
from neo4j.v1 import GraphDatabase, basic_auth
import json
import csv
import os
import time


t = time.time()


driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "Alien"))
session = driver.session()

query = "MATCH (n)-[r]->(m) where NOT r.rel_type= \"registered_address\" AND NOT r.rel_type =~ \"same*\" and NOT n.country_codes = m.country_codes WITH [n.country_codes, m.country_codes] as list return list"
table_inter = session.run(query);

couple = [" ", " "]
country_relation = {}
first = False;

for record in table_inter:
    for i in record["list"]:
        if(first):
            couple[1] = str(i)
            first = False
            for src in couple[0].split(';'):
                if src not in country_relation:
                    country_relation[src] = {}
                for dest in couple[1].split(';'):
                    if dest not in country_relation[src]:
                        country_relation[src][dest] = 0
                    country_relation[src][dest] += 1
        else:
            couple[0] = str(i)
            first = True

session.close()

print "CHN -> HKG = " + str(country_relation["CHN"]["HKG"])

t = time.time()-t
print t
