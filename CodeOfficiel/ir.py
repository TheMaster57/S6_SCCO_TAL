#!/usr/bin/env python
 
import re
 
# Le chemin vers le dossier contenant les fichiers de la Cranfield collection.
data_path = "./cran"
 
def read_docs():
    with open(data_path + "/cran.all.1400") as f:
        docs = re.findall(r"^\.I ([0-9]+)\n((?:.(?!\n\.I [0-9]+\n))*.)",\
                          f.read(), flags = re.M | re.S)
        id_body_pairs = map(lambda p: (int(p[0]), re.sub(r"^\.[TABW]\n", "\n",\
                                                         p[1],\
                                                         flags = re.M | re.S)),\
                            docs)
        return dict(id_body_pairs)
 
# Un dictionnaire qui donne pour un docID son contenu.
docs = read_docs()
 
def read_queries():
    with open(data_path + "/cran.qry") as f:
        queries = re.findall(r"^\.I [0-9]+\n.W\n((?:.(?!\n\.I [0-9]+\n))*.)",\
                             f.read(), flags = re.M | re.S)
        id_query_pairs = enumerate(queries, start = 1)
        return dict(id_query_pairs)
 
# Un dictionnaire qui relie les queryIDs et leurs contenus.
queries = read_queries()
 
def read_relevance():
    with open(data_path + "/cranqrel") as f:
        qd_pairs = map(lambda l: (int(l.split()[0]), int(l.split()[1])),\
                       f.readlines())
        return set(qd_pairs)
 
# Un ensemble des pairs (q,d) ou q est le queryID d'une question pour
# laquelle d est un docID d'un document qui lui est pertinent.
relevance = read_relevance()
 
def tokenize(text):
    return text.split()
 
# frequencies(["ab", "bc", "ab"]) = { "ab" : 2, "bc" : 1 }
# frequencies(tokenize(docs[1])) = { "slipstream": 6,
#                                    "configuration": 1,
#                                    ... }
 
def frequencies(toks):
    freqs = {}
    for tok in toks:
        if tok in freqs:
            freqs[tok] += 1
        else:
            freqs[tok] = 1
    return freqs
 
# build_index(...) = { "slipstream": [(1,6), (16,3), ...],
#                      "configuration": [(1,1), ...],
#                      ... }
 
def build_index(docs):
    """VOTRE CODE ICI

       A partir de la collection des documents, construisez une structure
       des donnees qui vous permettra d'identifier des documents pertinents
       pour une question (e.g., l'index inversee qu'on a vu en classe).
    """
    index = {}
 
    # for docID in docs:
    #     freqs = frequencies(tokenize(docs[docID]))
    #     ...
 
    return index
 
 
def rank_docs(docs, query, index):
    """VOTRE CODE ICI

       Retournez la serie des docIDs ordonnes par leur pertinence vis-a-vis
       la question 'query'.
    """
    return docs.keys()
 
 
 
def average_precision(qid, ranking):
    relevant = 0
    total = 0
    precisions = []
    
    for did in ranking:
        total += 1
        if (qid, did) in relevance:
            relevant += 1
            precisions.append(float(relevant) / float(total))
 
    return float(sum(precisions)) / float(len(precisions))
 
 
def uniqify(xs):
    seen = set()
    return [ x for x in xs if not (x in seen or seen.add(x)) ]
 
 
def mean_average_precision():
    index = build_index(docs)
    aps = []
 
    for qid in queries:
        ranking = rank_docs(docs, queries[qid], index)
        normalized_ranking = uniqify(list(ranking) + list(docs.keys()))
        aps.append(average_precision(qid, normalized_ranking))
 
    return float(sum(aps)) / float(len(aps))
 
# Imprime le MAP de l'approche implemente
print("Mean average precision: " + str(mean_average_precision()))
