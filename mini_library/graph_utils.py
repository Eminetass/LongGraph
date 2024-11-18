import networkx as nx
import matplotlib.pyplot as plt

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
        graph.add_edge(relation[0], relation[1])

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
