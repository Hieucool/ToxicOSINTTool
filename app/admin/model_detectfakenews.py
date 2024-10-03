import pickle
from .model_detect.cleanData import text_preprocess
# from .model_detect.crawlData import start_crawl
from flask import Flask, request, jsonify

import os

basedir = os.path.abspath(os.path.dirname(__file__))

def preprocess_text(text):
    text = text_preprocess(text)
    return text



def getDomain(url):
    split_url = url.split('/')
    return split_url[2]

def check_blacklist(domain):
    basedir = os.path.abspath(os.path.dirname(__file__))
    black = open(basedir+ "\\model_detect\\blacklist.txt").read().split("\n")
    for item in black:
        if(item in domain):
            return True
    
    return False


# def detect_fakenews(url):
#     domain = getDomain(url)
    
#     try:
#         text = start_crawl(url)
        
#     except Exception as e:
#         return str(e)
    
#     if(text != ""):
#         print("crawl thanh cong")
#         if(check_blacklist(domain)):
#             result = 'Danger news'
#         else:
#             MODEL_PATH = os.path.join(basedir, r"model_detect/naive_bayes.pkl")
#             model = pickle.load(open(MODEL_PATH, 'rb'))
#             print("Su dung model fakenews")

#             # Extract text content from URL
#             print("[debug]  ", text)
            
#             preprocessed_text = preprocess_text(text['content'])
#             # Predict label using the model
#             predicted_label = model.predict([preprocessed_text])[0]
#             if predicted_label == 1:
#                 result = 'Safe news'
#             else : result  = 'Danger news'
    
                
#         text['predicted_label'] = result
        
#         return text
    
#     return False


def detect_content(content):
    MODEL_PATH = os.path.join(basedir, r"model_detect/naive_bayes.pkl")
    model = pickle.load(open(MODEL_PATH, 'rb'))
    print("Su dung model fakenews")
    
    preprocessed_text = preprocess_text(content)
    # Predict label using the model
    predicted_label = model.predict([preprocessed_text])[0]
    if predicted_label == 1:
        result = False
    else : result  = True
    
    return result