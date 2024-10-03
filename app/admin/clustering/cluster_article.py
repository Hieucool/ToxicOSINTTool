import json
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
from copy import deepcopy

def generateBigram(paper):
    words = paper.split()
    if len(words) == 1:
        return ''
    bigrams = [words[i] + '_' + words[i+1] for i in range(0,len(words) - 1)]
    return ' '.join(bigrams)

def removeRedundant(text,redundantSet):
    words = text.split()
    for i in range(0,len(words)):
        if words[i].count('_') == 0 and (words[i] in redundantSet or words[i].isdigit()):
            words[i] = ''
        else:
            sub_words = words[i].split('_')
            if any(w in redundantSet or w.isdigit() for w in sub_words):
                words[i] = ''
    words = [w for w in words if w != '']
    words = ' '.join(words)
    return words
import os
basedir    = os.path.abspath(os.path.dirname(__file__))
stopwords = set(open(basedir+'/stopwords.txt',encoding="utf-8").read().split('\n')[:-1])
puct_set = set([c for c in '!"#$%&\'()*+,./:;<=>?@[\\]^`{|}~'])

def preprocessing(text):
    text = ' '.join(word_tokenize(text))
    text = text.lower()
    text = ' '.join(text.split())
    text = text + generateBigram(text)
    text = removeRedundant(text,puct_set | stopwords)
    # print(text)
    return text

def distance(vecs):
    vec1 = vecs[0]
    vecAll = vecs[1]
    Dis_matrix = pairwise_distances(vec1,vecAll,metric = 'cosine',n_jobs=1)
    Dis_matrix = Dis_matrix.astype(np.float16)
    return Dis_matrix

def chunks_vec(l, n):
    for i in range(0, l.shape[0], n):
        yield l[i:i + n]


def PhanCum(data):
    
    documents = [item.content for item in data]
    print ("Number of documents: ", len(documents))

    #pre-processing
    clean_documents = []

    for item in documents:
        doc = preprocessing(item)
        clean_documents.append(doc)
        
    vectorizer = TfidfVectorizer(token_pattern = "\S+", min_df = 2)
    vectors = vectorizer.fit_transform(clean_documents)

    svd = TruncatedSVD(n_components=48, n_iter=10, random_state=42)
    svd_vectors = svd.fit_transform(vectors)


    vector_chunks = list(chunks_vec(svd_vectors,1000))
    vector_chunks = [(i,svd_vectors) for i in vector_chunks]

    Dis_matrix = []
    for item_vector in vector_chunks:
        Dis_matrix.append(distance(item_vector))
    Dis_matrix = np.vstack(Dis_matrix)
    THRESHOLD = 0.5

    # Create graph
    
    graph = deepcopy(Dis_matrix)
    graph[graph <= THRESHOLD] = 2
    graph[graph != 2] = 0
    graph[graph == 2] = 1
    graph = graph.astype(np.int8)

    # Find connected components(Clusters)
    from scipy.sparse.csgraph import connected_components                                                 
    res = connected_components(graph,directed=False)

    from collections import OrderedDict
    num_cluster = res[0]
    cluster_labels = res[1]
    res_cluster = OrderedDict()

    for i in range(0,len(cluster_labels)):
        if cluster_labels[i] in res_cluster: res_cluster[cluster_labels[i]].append(i)                      
        else: res_cluster[cluster_labels[i]] = [i]

    res_cluster = [res_cluster[i] for i in range(0,num_cluster)]
    res_cluster = [sorted(r) for r in res_cluster if len(r) > 1]
    res_cluster.sort(key=len,reverse=True)

    print ("Số nhóm: ", len(res_cluster))
    print ("Số bài viết đã được phân nhóm: ", len([j for i in res_cluster for j in i]))                    
    print ("Số bài viết chưa được phân nhóm: ", len(documents) - len([j for i in res_cluster for j in i])) 
    
    clustered_indexes = [j for i in res_cluster for j in i]
    noise_cluster = [idx for idx in range(len(documents)) if idx not in clustered_indexes]

    
    result = []
    
    for i in range(0,len(res_cluster)):
        temp_cluster = {
            "name": "Cluster " + str(i),
            "data": []
        }
        print ("Cluster " + str(i))
        for idx in res_cluster[i]:
            print (data[idx].title, data[idx].url)
            temp_cluster['data'].append(data[idx])
        
        result.append(temp_cluster)
        print()

    print("Noise_cluster :")
    temp_cluster = {
        "name": "Noise_cluster",
        "data": []
    }
    for idx in noise_cluster:
        print (data[idx].title, data[idx].url)
        temp_cluster['data'].append(data[idx])
        
    result.append(temp_cluster)
    
    return result
    
# documents = []
# with open("result.json", "r", encoding="utf-8") as f:
#     data = json.load(f) 
    
# PhanCum(data)