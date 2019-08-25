"""
Process a list of object instances into dataframes in order to prepare them for
modeling 
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from datetime import date

def client_processing(clis): 
    clients = pd.DataFrame({"age": [],
                            "income": [],
                            "male": [],
                            "inv_expenses": [],
                            "days_active": [],
                            "credit_rating": [],
                            "children": [],
                            "education": [],
                            "portfolio": []})

    for client in clis:
        df = pd.DataFrame()

        df["age"] = client.age
        df["income"] = client.income
        df["male"] = client.male
        df["inv_expenses"] = client.inv_expenses
        td = pd.Timestamp(date.today()) - client.date_of_join
        df["days_active"] = td.days
        df["credit_rating"] = client.credit_rating
        df["children"] = client.children
        df["education"] = client.education
        df["portfolio"] = client.portfolio

        clients.append(df)

    return clients

def consultant_processing(cons):
    consultants = pd.DataFrame({"age": [],
                                "experience": [],
                                "days_active": [],
                                "n_clients": [],
                                "portfolio": []})

    for consultant in cons:
        df = pd.DataFrame()
        df["age"] = consultant.age
        df["experience"] = consultant.experience
        td = pd.Timestamp(date.today()) - consultant.date_of_join
        df["days_active"] = td.days
        df["n_clients"] = len(consultant.client_history)
        df["portfolio"] = consultant.portfolio

        consultants.append(df)

    return consultants

def portfolio_processing(ports):
    portfolios = pd.DataFrame({"volatility": [], 
                               "returns": [],
                               "n_transactions": [],
                               "eq_ratio": [],
                               "bond_ratio": [],
                               "com_ratio": []})
    for port in ports:
        df = pd.DataFrame()
        df["volatility"] = port.get_volatility()
        df["returns"] = port.get_returns()
        df["n_transactions"] = len(port.history)
        
        a_dict = {"equity":0, "bond":0, "commodity":0}

        for asset in port.assets:
            a_dict[asset.inv_type] += 1

        df["eq_ratio"] = a_dict["equity"] / len(port.assets)
        df["bond_ratio"] = a_dict["bond"] / len(port.assets)
        df["com_ratio"] = a_dict["commodity"] / len(port.assets)

        portfolios.append(df)

    return portfolios

def interaction_processing(inters, glob_avg):
    interactions = pd.DataFrame({"client":[],
                                 "consultant":[],
                                 "duration":[],
                                 "ongoing":[],
                                 "n_transactions":[],
                                 "score":[]})

    for interaction in inters:
        df = pd.DataFrame()

        df["client"] = interaction.client
        df["consultant"] = interaction.consultant
        end = interaction.end if interaction.end else pd.Timestamp(date.today())
        td = interaction.start - end
        df["duration"] = td.days
        df["ongoing"] = interaction.end is None
        df["n_interactions"] = len(interaction.transactions)

        if isinstance(glob_avg, list):
            # assumes this is a list of portfolios
            glob_avg = np.mean([p.get_returns for p in glob_avg])
        elif isinstance(glob_avg, pd.DataFrame):
            glob_avg = np.mean(glob_avg["returns"])

        df["score"] = interaction.score(glob_avg=glob_avg)

        interactions.append(df)

    return interactions
