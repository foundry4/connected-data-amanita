"""RDF Namespaces for Datalab"""
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, XSD, OWL, FOAF, DC, DCTERMS, SKOS
namespaces = {
    'rdf': RDF,
    'rdfs': RDFS,
    'xsd': XSD,
    'owl': OWL,
    'stardog': Namespace('tag:stardog:api:'),
    'dct': DCTERMS,
    'dcterms': DCTERMS,
    'po': Namespace('http://purl.org/ontology/po/'),
    'dc': DC,
    'event': Namespace('http://purl.org/NET/c4dm/event.owl#'),
    'foaf': FOAF,
    'frbr': Namespace('http://purl.org/vocab/frbr/core#'),
    'geo': Namespace('http://www.w3.org/2003/01/geo/wgs84_pos#'),
    'mo': Namespace('http://purl.org/ontology/mo/'),
    'bbcprov': Namespace('http://www.bbc.co.uk/ontologies/provenance/'),
    'skos': SKOS,
    'potags': Namespace('http://www.holygoat.co.uk/owl/redwood/0.1/tags/'),
    'tl': Namespace('http://purl.org/NET/c4dm/timeline.owl#'),
    'vs': Namespace('http://www.w3.org/2003/06/sw-vocab-status/ns#'),
    'schema': Namespace('http://schema.org/'),
    'datalab': Namespace('datalab:bbc.co.uk,2018/FIXME/')}
