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
            records = [record.data() for record in result]
            return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Close the Neo4j driver when the application shuts down
@app.teardown_appcontext
def close_driver(exception):
    driver.close()

if __name__ == '__main__':
    app.run(debug=True, port=5005)