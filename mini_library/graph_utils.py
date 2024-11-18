import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

def build_graph(entities, relations):
    """
    Varlıklar ve ilişkilerden bir bilgi grafiği oluşturur.
    """
    graph = nx.DiGraph()

    # Düğümleri ekle
    for entity in entities:
        graph.add_node(entity[0], label=entity[1])

    # Kenarları ekle
    for relation in relations:
        graph.add_edge(relation[0], relation[2], relation=relation[1]) 

    return graph

def visualize_graph(graph, title="Bilgi Grafiği"):
    """
    Bilgi grafiğini görselleştirir.
    """
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=10,
        font_weight="bold",
    )
    plt.title(title)
    plt.show()


def query_graph(graph, entity, relation=None):
    """
    Grafikten belirtilen varlık ve ilişkilerle ilgili sorgu yapar.
    
    Args:
        graph (nx.DiGraph): Bilgi grafiği.
        entity (str): Sorgulanacak düğüm.
        relation (str): Belirli bir ilişki türü (opsiyonel).
    
    Returns:
        List[str]: Sorgu sonuçları.
    """
    results = []
    for source, target, data in graph.edges(data=True):
        if source == entity and (relation is None or data.get("relation") == relation):
            results.append(target)
    return results



def save_to_neo4j(graph, uri, user, password):
    """
    Bilgi grafiğini Neo4j'e kaydeder.
    
    Args:
        graph (nx.DiGraph): Bilgi grafiği.
        uri (str): Neo4j bağlantı URI.
        user (str): Neo4j kullanıcı adı.
        password (str): Neo4j şifresi.
    """
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        session.write_transaction(lambda tx: create_graph_in_neo4j(tx, graph))
    driver.close()

def create_graph_in_neo4j(tx, graph):
    """
    Neo4j üzerinde düğümleri ve kenarları oluşturur.
    """
    for node, data in graph.nodes(data=True):
        tx.run("MERGE (n:Entity {name: $name, label: $label})", name=node, label=data.get("label"))

    for source, target, data in graph.edges(data=True):
        tx.run("""
            MATCH (a:Entity {name: $source}), (b:Entity {name: $target})
            MERGE (a)-[r:RELATION {type: $relation}]->(b)
        """, source=source, target=target, relation=data.get("relation"))