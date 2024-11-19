import spacy
import networkx as nx
import matplotlib.pyplot as plt

def load_text(state):
    """
    Kitap özetlerini dosyadan yükler.
    """
    with open("text_data.txt", "r") as file:
        state.text = file.read()
    return state

def extract_entities_and_relations(state):
    """
    Metinden varlıkları ve ilişkileri çıkarır.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(state.text)

    entities = []
    relations = []

    # Varlık çıkarımı
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # İlişki çıkarımı
    for token in doc:
        if token.dep_ == "ROOT":
            subject = [w.text for w in token.lefts if w.dep_ == "nsubj"]
            obj = [w.text for w in token.rights if w.dep_ == "dobj"]
            if subject and obj:
                relations.append((subject[0], token.text, obj[0]))

    state.entities = entities
    state.relations = relations
    return state

def build_and_visualize_graph(state):
    """
    Bilgi grafiği oluşturur ve görselleştirir.
    """
    graph = nx.DiGraph()

    # Düğümleri ekle
    for entity in state.entities:
        graph.add_node(entity[0], label=entity[1])

    # Kenarları ekle
    for relation in state.relations:
        graph.add_edge(relation[0], relation[2], label=relation[1])

    # Grafiği görselleştir
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=3000, font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, "label"))
    plt.title("Kitap Bilgi Grafiği")
    plt.show()

    return state
