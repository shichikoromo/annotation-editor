#app/aif_handler.py
from rdflib import Graph, Namespace, URIRef, RDF, Literal, RDFS
from typing import Optional

class AIFBuilder:
    def __init__(self, file_namespace: str):
        self.aif_ns = Namespace("AIF/")
        self.ns_str = file_namespace if file_namespace.endswith("/") else file_namespace + "/"
        self.namespace = Namespace(self.ns_str)
        self.graph = Graph()
        self.graph.bind("rdf", RDF)
        self.graph.bind("AIF", self.aif_ns)

    def add_argument(self, source_id: str, target_id: str, relation: str):

        source_uri = URIRef(f"{self.ns_str}{source_id.split('_')[1]}")
        target_uri = URIRef(f"{self.ns_str}{target_id.split('_')[1]}")

        self.graph.add((source_uri, RDF.type, self.aif_ns.Premise))
        self.graph.add((target_uri, RDF.type, self.aif_ns.Conclusion))

        self.graph.add((source_uri, self.aif_ns[relation], target_uri))

    def build_aif(self, arguments: list[dict]):
        for arg in arguments:
            self.add_argument(
                source_id=arg.i_source_id,
                target_id=arg.i_target_id,
                relation=arg.s_relation
            )

    def serialize(self) -> str:
        return self.graph.serialize(format="pretty-xml", encoding="utf-8",max_depth=1).decode("utf-8")
