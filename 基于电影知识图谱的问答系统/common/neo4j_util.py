from py2neo import Graph

neo4j_url = "http://localhost:7474"
user = "neo4j"
password = "19980524lzh5"
def connect_neo4j():
    neo4j = Graph(neo4j_url,user=user,password=password)
    return neo4j

class Neo4jQuery:
    def __init__(self):
        self.graph =connect_neo4j()
    def run(self,cql):
        result = []
        res = self.graph.run(cql)
        for i in res:
            result.append(i.items()[0][1])
        return result

if __name__ =="__main__":
    neo = Neo4jQuery()
    res = neo.run('MATCH (n:Movie)-[]->() WHERE n.title="花样年华" return n.rating')
    print(res)