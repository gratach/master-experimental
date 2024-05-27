from random import randint, choice, shuffle
from json import loads, dumps
from lib import gpt_3_5_turbo_completion, gpt_4_turbo_completion, tryRecieveAnswer
def getSemanticTriples(subjectTerm):
    querry = f'Semantic triples such as ["Star", "emits", "Light"] and ["Rocket", "can bring cargo to", "Space"] consists of a subject, a predicate, and an object. Give me five examples of semantic triples that contain "{subjectTerm}" as subject and return them in an array formatted like [["sub1", "pred1", "obj1"], ["sub2", "pred2", "obj2"], ...]. Return nothing but the array without explanation.'
    def answerConversion(answer):
        result = loads(answer)
        assert isinstance(result, list)
        assert all(isinstance(triple, list) for triple in result)
        assert all(len(triple) == 3 for triple in result)
        assert all(isinstance(term, str) for triple in result for term in triple)
        return result
    answer, success = tryRecieveAnswer(querry, gpt_4_turbo_completion, answerConversion)
    if success:
        return answer
    return None

def tripleRandomWalk(startSubject):
    triples = []
    currentSubject = startSubject
    while input() == "":
        nextTriple = choice(getSemanticTriples(currentSubject))
        triples.append(nextTriple)
        currentSubject = nextTriple[2]
    return triples