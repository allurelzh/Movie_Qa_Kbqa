from common import neo4j_util
movie_neo4j = neo4j_util.connect_neo4j()
def load_genre():
    genre_node_cql ='''LOAD CSV WITH HEADERS FROM "file:///genre.csv" AS line
    MERGE(p:Genre{gid:toInteger(line.gid),gname:line.gname})
    '''
    movie_neo4j.run(genre_node_cql)

def load_person():
    person_node_cql ='''LOAD CSV WITH HEADERS FROM
    "file:///person.csv" AS line MERGE(p:Person{pid:toInteger(line.pid),birth:line.birth,
    death:line.death,name:line.name,biography:line.biography,birthplace:line.birthplace})
    '''
    movie_neo4j.run(person_node_cql)

def load_movie():
    movie_node_cql ='''LOAD CSV WITH HEADERS FROM "file:///movie.csv" AS line
    MERGE(p:Movie{mid:toInteger(line.mid),title:line.title,introduction:line.introduction,rating:toFloat(line.rating),releasedate:line.releasedate})
    '''
    movie_neo4j.run(movie_node_cql)

def load_movie_person_rel():
    movie_person_rel='''LOAD CSV WITH HEADERS FROM
    "file:///person_to_movie.csv" AS line match(from:Person{pid:toInteger(line.pid)}),
    (to:Movie{mid:toInteger(line.mid)}) merge (from)-[r:actedin{pid:toInteger(line.pid),mid:toInteger(line.mid)}]->(to)
    '''
    movie_neo4j.run(movie_person_rel)
def load_movie_genre_rel():
    movie_genre_rel = '''LOAD CSV WITH HEADERS FROM "file:///movie_to_genre.csv" AS line
    match (from:Movie{mid:toInteger(line.mid)}),(to:Genre{gid:toInteger(line.gid)})
    merge (from)-[r:is{mid:toInteger(line.mid),gid:toInteger(line.gid)}]->(to)
    '''
    movie_neo4j.run(movie_genre_rel)