from flask import Flask, json, render_template
from neo4j.v1 import GraphDatabase, basic_auth

app = Flask(__name__)

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "yt"))

session = driver.session()

Addresses = session.run("match (n:Addresses) return count(*)").single().values()[0]
Entities = session.run("match (n:Entities) return count(*)").single().values()[0]
Intermediaries = session.run("match (n:Intermediaries) return count(*)").single().values()[0]
Officers = session.run("match (n:Officers) return count(*)").single().values()[0]

base = {}
base["Addresses"] = str(Addresses)
base["Entities"] = str(Entities)
base["Intermediaries"] = str(Intermediaries)
base["Officers"] = str(Officers)

@app.route("/")
def home():
    return "Usage : /visu or /data/count/<type> or data/count"

@app.route("/visu")
def visu():
    return render_template("panama-visu.html", data = base)

@app.route("/data/count/<type>")
def data_count(type):
    if type in base:
        s = "match (n: %s) return count(*)"%(type)
        value = session.run(s).single().values()[0]
        return "Number of nodes in " + type + ": " + str(value)
    else:
        return "Invalid type"

@app.route("/data/count")
def data():
    return json.dumps(base)

session.close()

if __name__ == "__main__":
    app.run()

