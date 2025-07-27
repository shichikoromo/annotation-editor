#app/rdf_handler.py
from rdflib import Graph, Namespace, URIRef, Literal, RDF

class RDFBuilder:
    def __init__(self, file_namespace: str):
        self.ns_str = file_namespace if file_namespace.endswith("/") else file_namespace + "/"
        self.namespace = Namespace(self.ns_str)
        self.graph = Graph()
        #self.graph.bind(self.ns_str, self.namespace)
        self.graph.bind(file_namespace, self.namespace)


    def build_statement(self, statement_id: str, subject: str, predicate: str, object_: str, sentence: str):
        statement_uri = URIRef(self.ns_str + f"statement_{statement_id}")
        subj_uri = URIRef(self.ns_str + subject)
        pred_uri = URIRef(self.ns_str + predicate)
        obj_uri = URIRef(self.ns_str + object_)

        self.graph.add((statement_uri, RDF.type, RDF.Statement))
        self.graph.add((statement_uri, RDF.subject, subj_uri))
        self.graph.add((statement_uri, RDF.predicate, pred_uri))
        self.graph.add((statement_uri, RDF.object, obj_uri))
        self.graph.add((statement_uri, self.namespace.source_text, Literal(sentence)))

    def build_rdf(self, annotations: list[dict]):
        for ann in annotations:
            self.build_statement(
                statement_id=ann.rdf_id,
                subject=ann.subject,
                predicate=ann.predicate,
                object_=ann.object_,
                sentence=ann.sentence
            )

    def serialize(self) -> str:
        return self.graph.serialize(format="application/rdf+xml", encoding="utf-8").decode("utf-8")#"application/rdf+xml", encoding="utf-8").decode("utf-8")
