import spacy
from graph_utils import build_graph, visualize_graph

def process_text(file_path):
    """
    Metni dosyadan yükler ve döndürür.
    """
    with open(file_path, "r") as file:
        text = file.read()
    return text

def extract_entities_and_relations(text):
    """
    Metindeki varlıkları (entities) ve ilişkileri (relations) çıkarır.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    entities = []
    relations = []

    # Varlık çıkarımı
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # İlişki çıkarımı
    for token in doc:
        if token.dep_ == "ROOT":  # Cümlenin kök fiilini bul
            subject = [w.text for w in token.lefts if w.dep_ == "nsubj"]  # Özneyi bul
            obj = [w.text for w in token.rights if w.dep_ == "dobj"]  # Nesneyi bul
            if subject and obj:
                relations.append((subject[0], token.text, obj[0]))

    return entities, relations


if __name__ == "__main__":
    # 1. Metni yükle
    text = process_text("text_data.txt")

    # 2. Varlıkları ve ilişkileri çıkar
    entities, relations = extract_entities_and_relations(text)

    # 3. Çıkarılan verileri ekrana yazdır
    print("Varlıklar (Entities):", entities)
    print("İlişkiler (Relations):", relations)

    # 4. Bilgi grafiğini oluştur
    graph = build_graph(entities, relations)

    # 5. Bilgi grafiğini görselleştir
    visualize_graph(graph, title="Mini Kütüphane Bilgi Grafiği")
