import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from processing import *

def build_port_model(data):

    X = np.array(data)
    model = KMeans(n_clusters=5).fit(X)
    return model

def build_cons_model(data):
    X = np.array(data)
    model = KMeans(n_clusters=10).fit(X)
    return model

def classify_consultors(model, consultors):
    
    consultors["class"] = model.predict(constructors)

def classify_portfolios(model, portfolios):
    
    constructors["class"] = model.predict(portfolios)

def sub_port_in_cons(model, consultors):
    
    for i in range(len(consultors)-1):
        consultors["portfolio"][i] = model.predict( \
                                        portfolio_processing( \
                                            [consultors["portfolio"]]))

    return consultors

def match_processing(port_model, cons_model, interactions):
    interactions["consultant"] = classify_consultor(cons_model, 
                                                    consultant_processing( \
                                                        interactions["consultant"]))["class"]

    # not good, add portfolio
    interactions.concat(classify_portfolios(port_model, 
                                            portfolio_processing( \
                                                [i.client.portfolio for i in interactions])))

    del interactions["client"]

    return interactions

def build_matcher(data):
    
    models = {}

    for group in data.group_by("consultant"):
        X = np.array(data.drop(["consultant", "score"]))
        y = np.array(data["score"]).reshape(-1, 1)
        models[group[0]] = LinearRegression().fit(X, y)

    return models

def match(client, match_models):
    model_results = {}

    for category, model in match_models:
        model_results[category] = model.predict(client_processing(client))

    return model_results
