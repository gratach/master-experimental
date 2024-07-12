from pathlib import Path
datapath = Path("../master-database-files/master-experimental/physics_ontology/")
from rdflib import Graph, URIRef, Literal, Namespace, term
ontoGraph = Graph() # Ontology graph
ontoGraph.parse(str(datapath / "physci.nt"))
indiGraph = Graph() # Individual graph

def getAllClasses(graph):
    qres = graph.query(
        """SELECT ?s
           WHERE {
              ?s a owl:Class
              }""")
    classes = []
    for row in qres:
        if type(row.s) == term.BNode:
            continue
        classes.append(str(row.s))
    return classes
def getNodeName(graph, iri):
    return iri.replace("/", "#").split("#")[-1]
def getNodeDescription(graph, iri):
    qres = graph.query(
        """SELECT ?description
           WHERE {
              ?s <http://purl.org/dc/elements/1.1/description> ?description.
           }""", initBindings = {'s': URIRef(iri)})
    for row in qres:
        return row.description.value
def getNodeComment(graph, iri):
    qres = graph.query(
        """SELECT ?comment
           WHERE {
              ?s rdfs:comment ?comment.
           }""", initBindings = {'s': URIRef(iri)})
    for row in qres:
        return row.comment.value
def getSuperClasses(graph, iri):
    qres = graph.query(
        """SELECT ?superclass
           WHERE {
              ?s rdfs:subClassOf ?superclass.
              }""", initBindings = {'s': URIRef(iri)})
    superclasses = set()
    for row in qres:
        superclasses.add(str(row.superclass))
    returnSuperclasses = set()
    for superclass in superclasses:
        returnSuperclasses.add(superclass)
        returnSuperclasses = returnSuperclasses.union(getSuperClasses(graph, superclass))
    return returnSuperclasses
def getPropertyTriplesWithSubject(graph, iri):
    superclasses = getSuperClasses(graph, iri)
    triples = []
    for superclass in (superclasses | {iri}):
        qres = graph.query(
            """SELECT ?predicate ?object
                WHERE {
                    ?predicate a owl:ObjectProperty.
                    ?predicate rdfs:domain ?subject.
                    ?predicate rdfs:range ?object.
                }""", initBindings = {'subject': URIRef(superclass)})
        for row in qres:
            triples.append((superclass, str(row.predicate), str(row.object)))
    return triples
def getPropertyTriplesWithObject(graph, iri):
    superclasses = getSuperClasses(graph, iri)
    triples = []
    for superclass in (superclasses | {iri}):
        qres = graph.query(
            """SELECT ?predicate ?subject
                WHERE {
                    ?predicate a owl:ObjectProperty.
                    ?predicate rdfs:domain ?subject.
                    ?predicate rdfs:range ?object.
                }""", initBindings = {'object': URIRef(superclass)})
        for row in qres:
            triples.append((str(row.subject), str(row.predicate), superclass))
    return triples

# Start navigation
classes = getAllClasses(ontoGraph)
while True:
    # Print all classes
    print("All classes in the ontology:")
    for i, class_ in enumerate(classes):
        print(f"{i+1}. {getNodeName(ontoGraph, class_)}")
    classByName = {getNodeName(ontoGraph, class_): class_ for class_ in classes}
    # Select a class
    selection = input("Enter the number or name of the class you want to explore: ")
    if selection.isdigit():
        selection = classes[int(selection)-1]
    else:
        selection = classByName[selection]
    # Repeat navigation iteration
    while True:
        print(f"Selected class: {getNodeName(ontoGraph, selection)}")
        print(f"Description: {getNodeDescription(ontoGraph, selection)}")
        print(f"Comment: {getNodeComment(ontoGraph, selection)}")
        # Print enumerated properties
        print("Properties:")
        propertyTriplesWithSubject = getPropertyTriplesWithSubject(ontoGraph, selection)
        for i, triple in enumerate(propertyTriplesWithSubject):
            print(f"{i+1}: <self> ({getNodeName(ontoGraph, triple[1])}) {getNodeName(ontoGraph, triple[2])}")
        propertyTriplesWithObject = getPropertyTriplesWithObject(ontoGraph, selection)
        for i, triple in enumerate(propertyTriplesWithObject):
            print(f"{i+1+len(propertyTriplesWithSubject)}: {getNodeName(ontoGraph, triple[0])} ({getNodeName(ontoGraph, triple[1])}) <self>")
        input_ = input("Enter the number of the property you want to explore 'back' to select another class or 'exit' to exit: ")
        if input_ == "back":
            break
        if input_ == "exit":
            exit()
        input_ = int(input_) - 1
        if input_ < len(propertyTriplesWithSubject):
            selection = propertyTriplesWithSubject[input_][2]
        else:
            selection = propertyTriplesWithObject[input_ - len(propertyTriplesWithSubject)][0]

