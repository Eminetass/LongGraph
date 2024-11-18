from fastapi import FastAPI
from graph_utils import build_graph, query_graph
from fastapi.responses import JSONResponse

app = FastAPI()

# Örnek grafiği yükle
entities = [('1984', 'WORK_OF_ART'), ('George Orwell', 'PERSON')]
relations = [('1984', 'written_by', 'George Orwell')]

graph = build_graph(entities, relations)

@app.get("/query")
def query(entity: str, relation: str = None):
    results = query_graph(graph, entity, relation)
    return JSONResponse(content={"results": results})
