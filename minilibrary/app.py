from langgraph import StateGraph, Node
from graph_utils import load_text, extract_entities_and_relations, build_and_visualize_graph

def create_library_graph() -> StateGraph:
    """
    LangGraph ile kitap bilgi grafiği iş akışını oluşturur.
    """
    graph = StateGraph()

    # İş akışı düğümleri
    graph.add_node(Node(name="load_text", func=load_text))
    graph.add_node(Node(name="extract_entities_and_relations", func=extract_entities_and_relations))
    graph.add_node(Node(name="build_and_visualize_graph", func=build_and_visualize_graph))

    # Düğüm bağlantıları
    graph.add_edge("load_text", "extract_entities_and_relations")
    graph.add_edge("extract_entities_and_relations", "build_and_visualize_graph")

    return graph
