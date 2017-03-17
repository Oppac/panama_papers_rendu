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

# Create Addresses
session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"File:///Addresses.csv\" AS row "\
            "CREATE (:Address :Global {address: row.address, icij_ij: row.icij_id, valid_until: row.valid_until, "\
            "country_codes: row.country_codes, countries: row.countries, node_id: toInt(row.node_id), sourceID: row.sourceID, note: row.note})")
# Enforce some integrety
session.run("create constraint on (o:Address) assert o.node_id is unique")

# Create Entities
session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"File:///Entities.csv\" AS row "\
            "CREATE (:Entity :Global {name: row.name, original_name: row.original_name, former_name: row.former_name, "\
            "jurisdiction: row.jurisdiction, jurisdiction_description: row.jurisdiction_description, "\
            "company_type: row.company_type, address: row.address, internal_id: row.internal_id, incorporation_date: row.incorporation_date, "\
            "inactivation_date: row.inactivation_date, struck_off_date: row.struck_off_date, dorm_date: row.dorm_date, status: row.status, "\
            "service_provider: row.service_provider, ibcRUC: row.ibcRUC, country_codes: row.country_codes, countries: row.countries, "\
            "note: row.note, valid_until: row.valid_until, node_id: toInt(row.node_id), sourceID: row.sourceID})")
# Enforce some integrety
session.run("create constraint on (o:Entity) assert o.node_id is unique")

# Create Intermediaries
session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"File:///Intermediaries.csv\" AS row "\
            "CREATE (:Intermediary :Global {name: row.name, internal_id: row.internal_id, address: row.address, "\
            "valid_until: row.valid_until, country_codes: row.country_codes, countries: row.countries, "\
            "status: row.status, node_id: toInt(row.node_id), sourceID: row.sourceID, note: row.note})")
# Enforce some integrety
session.run("create constraint on (o:Intermediary) assert o.node_id is unique")

# Create Officers
session.run("USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"File:///Officers.csv\" AS row "\
            "CREATE (:Officer :Global {name: row.name, icij_id: row.icij_id, valid_until: row.valid_until, "\
            "country_codes: row.country_codes, countries: row.countries, node_id: toInt(row.node_id), sourceID: row.sourceID, note: row.note})")
# enforce some integrety
session.run("create constraint on (o:Officer) assert o.node_id is unique")


#session.run("create constraint on (o:Global) assert o.node_id is unique")

#session.run("CREATE INDEX ON :Address(node_id)")
session.run("CREATE INDEX ON :Address(countries)")

#session.run("CREATE INDEX ON :Entity(node_id)")
session.run("CREATE INDEX ON :Entity(name)")
session.run("CREATE INDEX ON :Entity(countries)")

#session.run("CREATE INDEX ON :Intermediary(node_id)")
session.run("CREATE INDEX ON :Intermediary(name)")
session.run("CREATE INDEX ON :Intermediary(countries)")

#session.run("CREATE INDEX ON :Officer(node_id)")
session.run("CREATE INDEX ON :Officer(name)")
session.run("CREATE INDEX ON :Officer(countries)")

session.run("CREATE INDEX ON :Global(node_id)")

t = time.time()-t
print "Add Nodes: " + str(t)

t = time.time()

with open('edges_type.json') as data_file:
	data = json.load(data_file)
os.system('rm -rf edges')
os.system('mkdir edges > /dev/null 2>&1')

input_file = open('all_edges.csv', 'r')
edges_reader = csv.reader(input_file)
init_row = edges_reader.next()

file_open = {}

for row in edges_reader:
	new = data[row[1]]
	name = new.split("/")
	for clean_name in name:
		row[1] = row[1].replace(row[1], clean_name)
		if 'edges/'+clean_name+'.csv' not in file_open:
			file_open['edges/'+clean_name+'.csv'] = open('edges/'+clean_name+'.csv', 'a+')
			f = file_open['edges/'+clean_name+'.csv']
			f_writer = csv.writer(f)
			f_writer.writerow(init_row)
		else:
			f = file_open['edges/'+clean_name+'.csv']
		f_writer = csv.writer(f)
		f_writer.writerow(row)

input_file.close()
for i in file_open.values():
	i.close()

t = time.time()-t
print "Clean Edges: " + str(t)

t = time.time()

os.system('ls edges > ls_folder.csv')
input_file = open('ls_folder.csv', 'r')
edges_reader = csv.reader(input_file)


def import_edges(edge_file):
    edge_type = edge_file.replace(".csv", "")
    query = "USING PERIODIC COMMIT LOAD CSV WITH HEADERS FROM \"file:///edges/"+edge_file+"\" AS row "\
            "MATCH (from: Global {node_id: toInt(row.node_1)}), (to: Global {node_id: toInt(row.node_2)}) "\
            "CREATE (from)-[:Relationship {rel_type: row.rel_type, sourceID: row.sourceID, valid_until: row.valid_until, start_date: row.start_date, end_date: row.end_date}]->(to)"
    session.run(query)

for edge_file in edges_reader:
    import_edges(edge_file[0])

session.close()

t = time.time()-t
print "Load Edges: " + str(t)
