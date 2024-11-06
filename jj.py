# from neo4j import GraphDatabase
# from config import cfg

# # Neo4j connection details
# uri = cfg["uri"]
# uname = cfg["username"]
# pwd = cfg["password"]
# db = cfg["database"]

# # cypher_query = """
# # MATCH (actor:Person {name: $actorName})-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(p: Person)
# # RETURN p.name as coActorName
# # """

# jj_query = "MATCH (n:Person)-[:ACTED_IN]->(m:Movie) WHERE m.title = 'As Good as It Gets' OR m.title = 'Speed Racer'  RETURN n as Actors"


# with GraphDatabase.driver(uri,auth=(uname, pwd)) as driver:
#     result = driver.execute_query(
#         jj_query,
#         # actorName="Tom Hanks",
#         # database_="movies"
#         )
#     for record in result.records:
#         print(record[0])

#     # for record in result.records:
#     #     node = record[0]
#     #     if isinstance(node, node):
#     #         print(node["name"])


from flask import Flask, render_template, request, jsonify
from neo4j import GraphDatabase
from config import cfg

app = Flask(__name__)

# Neo4j connection details
uri = cfg["uri"]
username = cfg["username"]
password = cfg["password"]

# Create Neo4j driver
driver = GraphDatabase.driver(uri, auth=(username, password))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query_neo4j():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        with driver.session() as session:
            result = session.run(query)
            nodes = []
            relationships = []
            for record in result:
                for key, value in record.items():
                    if isinstance(value, dict) and 'id' in value:
                        if value['id'] not in [node['id'] for node in nodes]:
                            nodes.append(value)
                    elif isinstance(value, dict) and 'startNode' in value and 'endNode' in value:
                        relationships.append(value)
            return jsonify({'nodes': nodes, 'relationships': relationships})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Close the Neo4j driver when the application shuts down
@app.teardown_appcontext
def close_driver(exception):
    driver.close()

if __name__ == '__main__':
    app.run(debug=True, port=5005)
