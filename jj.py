from neo4j import GraphDatabase
from config import cfg

# Neo4j connection details
uri = cfg["uri"]
uname = cfg["username"]
pwd = cfg["password"]
db = cfg["database"]

# cypher_query = """
# MATCH (actor:Person {name: $actorName})-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(p: Person)
# RETURN p.name as coActorName
# """

jj_query = "MATCH (n:Person)-[:ACTED_IN]->(m:Movie) WHERE m.title = 'As Good as It Gets' OR m.title = 'Speed Racer'  RETURN n as Actors"


with GraphDatabase.driver(uri,auth=(uname, pwd)) as driver:
    result = driver.execute_query(
        jj_query,
        # actorName="Tom Hanks",
        # database_="movies"
        )
    for record in result.records:
        print(record[0])

    # for record in result.records:
    #     node = record[0]
    #     if isinstance(node, node):
    #         print(node["name"])