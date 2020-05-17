import unicodedata
import json
import requests
import sqlite3
import torch
import numpy as np
import DBWrapper as db

# BERT imports
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel, BertForMaskedLM, AutoModel, AutoTokenizer

# ELSEVIER imports
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch

# NLTK imports
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# GLOBAL variable setup

'''
API SETUP 
'''
API_KEY = "32cb8485b0eda5d1c91c98d1acbb8f01"
client = ElsClient(API_KEY)
abstractURL = "https://api.elsevier.com/content/abstract/doi/"
API_headers = {'Accept': 'application/json', 'X-ELS-APIKey': API_KEY}


'''
DATABASE SETUP
'''
database = "CaseDatabase.db"

# Create SQLite connection
conn = sqlite3.connect(database)
cursor = conn.cursor()
colRetrieve = ["_index", "ID", "title", "question", "answer"]
colInsert = ["title_1", "abstract_1", "author_1", "source_1", "sourceURL_1"]
colInsert += ["title_2", "abstract_2", "author_2", "source_2", "sourceURL_2"]
colInsert += ["title_3", "abstract_3", "author_3", "source_3", "sourceURL_3"]
colInsert += ["title_4", "abstract_4", "author_4", "source_4", "sourceURL_4"]
colInsert += ["title_5", "abstract_5", "author_5", "source_5", "sourceURL_5"]

'''
BERT SETUP
'''
useModel = "allenai/scibert_scivocab_uncased"
tokenizer = AutoTokenizer.from_pretrained(useModel)
model = AutoModel.from_pretrained(useModel)

'''
NLTK SETUP
'''
stopWords = set(stopwords.words("english"))


# ------------------------------------------------------
# Database Functions
# ------------------------------------------------------
def retrieveRowCount():
    data = db.count(conn)
    count = data[0][0]
    return count


def retrieveRow(i):
    row = db.fetchRow(conn, i)
    row = row[0]
    data = {}
    for i in range(len(colRetrieve)):
        data[colRetrieve[i]] = row[i]
    return data


def updateRow(i, values):
    db.updateRow(conn, i, colInsert, values)


def retrieveQuestions():
    questions = []
    data = db.fetch(conn, "question")
    for d in data:
        questions.append(d[0])
    return questions


def filterStopwords(sentence):
    filtered = []
    words = word_tokenize(sentence)

    for w in words:
        if w.lower() not in stopWords:
            filtered.append(w)

    return " ".join(filtered)

# ------------------------------------------------------
# BERT functions
# ------------------------------------------------------


def bert(text_1, text_2):
    if (len(text_2) > 1500):
        text_2 = text_2[0:1500]

    marked_text_1 = "[CLS] " + text_1 + "[SEP]"
    tokenized_text_1 = tokenizer.tokenize(marked_text_1)
    indexed_tokens_1 = tokenizer.convert_tokens_to_ids(tokenized_text_1)
    segment_ids_1 = [0]*len(tokenized_text_1)
    tokens_tensor_1 = torch.tensor([indexed_tokens_1])
    segment_tensors_1 = torch.tensor([segment_ids_1])
    with torch.no_grad():
        encoded_layers_1, _ = model(tokens_tensor_1, segment_tensors_1)

    marked_text_2 = "[CLS] " + text_2 + "[SEP]"
    tokenized_text_2 = tokenizer.tokenize(marked_text_2)
    indexed_tokens_2 = tokenizer.convert_tokens_to_ids(tokenized_text_2)
    segment_ids_2 = [0]*len(tokenized_text_2)
    tokens_tensor_2 = torch.tensor([indexed_tokens_2])
    segment_tensors_2 = torch.tensor([segment_ids_2])
    with torch.no_grad():
        encoded_layers_2, _ = model(tokens_tensor_2, segment_tensors_2)

    sent_embedding_1 = encoded_layers_1[0].mean(axis=0)
    sent_embedding_2 = encoded_layers_2[0].mean(axis=0)
    sim_score = cosine_similarity(sent_embedding_1.reshape(
        1, -1), sent_embedding_2.reshape(1, -1))
    return sim_score


# ------------------------------------------------------
# API functions
# ------------------------------------------------------
def apiCall(query):
    results = []
    searchResult = ElsSearch(query, 'sciencedirect')

    # Check if API reuturns valid reults
    try:
        searchResult.execute(client, get_all=False)
    except:
        return results

    for result in searchResult.results:
        # Attempt to retrieve abstract

        try:
            DOI = result["prism:doi"]
            abstractResp = requests.get(
                url=abstractURL+DOI, headers=API_headers)
            abstractData = json.loads(abstractResp.text)

            # If valid abstract found then exract required data
            abstract = abstractData["abstracts-retrieval-response"]["coredata"]["dc:description"]
            author = result["dc:creator"]
            title = result["dc:title"]
            source = result["prism:publicationName"]
            sourceURL = result["prism:url"]

            results.append({
                "abstract": abstract,
                "author": author,
                "title": title,
                "source": source,
                "sourceURL": sourceURL
            })

        except:
            pass

        if (len(results) == 5):
            break

    return results
