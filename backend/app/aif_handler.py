#app/aif_handler.py
from rdflib import Graph, Namespace, URIRef, RDF, Literal

class AIFBuilder:
    def __init__(self, file_namespace: str):
        self.ns_str = file_namespace if file_namespace.endswith("/") else file_namespace + "/"
        self.namespace = Namespace(self.ns_str)
        self.graph = Graph()
        #self.graph.bind(self.ns_str, self.namespace)
        #self.graph.bind(file_namespace, self.namespace)
        self.graph.bind("rdf", RDF)
        self.graph.bind("AIF", self.aif_ns)

    def add_node(self, sentence_id: str, role: str, supports: list[str] = None):
        node_uri = URIRef(self.ns_str + f"statement{sentence_id}")
        node_class = self.aif_ns[role]

        self.graph.add((node_uri, RDF.type, node_class))

        if role == "Premise" and supports:
            target_uri = URIRef(self.ns_str + f"statement{supports}")
            self.graph.add((node_uri, self.aif_ns.supports, target_uri))

    def build_aif(self, annotations: list[dict]):
        for ann in annotations:
            self.add_node(
                rdf_id=ann.rdf_id,
                role=ann.type, 
                supports=ann.supports
            )

    def serialize(self) -> str:
        return self.graph.serialize(format="application/rdf+xml", encoding="utf-8").decode("utf-8")
