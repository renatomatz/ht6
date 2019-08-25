import pandas as pd

from numpy.random import randint, random
from datetime import date
from import_data import Equity, Custom

def random_transaction(income, start):
    n_days = (pd.Timestamp(date.today()) - start)
    d8 = start + pd.Timedelta(n_days, "days")
    ammount = income * (random() / 10)
    return (str(d8), ammount)


def random_client(name, age_r=(0, 100), income_r=(0, 1000000000), date_of_join_r=(pd.Timestamp("2000"), pd.Timestamp(date.today())), credit_rating_r=(0, 850), intended_investment_rat=0.2, n_transactions=(0, 100), children_r=(0,4), education_r=(0, 4)):

    client = {"name": name}

    client["age"] = randint(*age_r)
    client["income"] = randint(*income_r)
    client["sex"] = randint(0, 1)
    client["expenses"] = client["income"] * random()
    days = (date_of_join_r[1] - date_of_join_r[0]).days
    days = randint(days)
    client["date_of_join"] = str(date_of_join_r[0] + pd.Timedelta(days, "days"))
    client["credit_rating"] = randint(*credit_rating_r)
    client["intended_investment"] = client["income"] * random()*intended_investment_rat
    client["children"] = randint(*children_r)
    client["education"] = randint(*education_r)

    return client


def random_consultant(name, age_r=(0, 100), experience_r=(0, 45), date_of_join_r=(pd.Timestamp("2000"), pd.Timestamp(date.today()))):
    
    consultant = {"name": name}

    consultant["age"] = randint(*age_r)
    consultant["experience"] = randint(*experience_r)
    days = (date_of_join_r[1] - date_of_join_r[0]).days
    days = randint(days)
    consultant["date_of_join"] = str(date_of_join_r[0] + pd.Timedelta(days, "days"))

    return consultant


def random_portfolio(name, income, start, n_eq=(0, 3), n_bonds=(0, 3), n_com=(0, 3), n_transactions=(0, 100)):
    
    portfolio = {"name": name}

    equities = ["XOM", "WMT"][randint(*n_eq):]
    bonds = ["DGS10", "DGS30"][randint(*n_bonds):]
    commodities = ["GLD", "USO"][randint(*n_com):]

    asset_list = []

    for e in equities:
        asset_list.append(Equity(e, mem_file="data/assets", key="key.txt"))

    for b in bonds:
        bond = Custom(inv_type="bond", 
                      mem_file="data/assets", 
                      key="key.txt")
        asset_list.append(bond.get_dataset(b, source="fred", date_col="DATE"))

    for c in commodities:
        commodity = Custom(inv_type="commodity", 
                                 mem_file="data/assets", 
                                 key="key.txt")
        asset_list.append(commodity.get_dataset(c, columns="Close"))

    assets = {}

    for a in asset_list:
        # weights will be evenly distributed with fair chances of being bigger
        # and smaller than average
        if all(a == asset_list[-1]):
            assets[1 - sum([*assets.keys()])] = a
        else:
            assets[random() / (len(asset_list)-1)] = a

    history = pd.DataFrame({"date": [], "ammount": []})

    for _ in range(randint(*n_transactions)):
        t = random_transaction(income, start)
        history.append(pd.DataFrame({"date": t[0], "ammount": t[1]}))
        
    portfolio["assets"] = assets
    portfolio["history"] = history

    return portfolio

    
def random_interaction(name, clients, consultants, start_time=(pd.Timestamp("2000"), pd.Timestamp(date.today()))):
    
    return {"name": name,
            "client": clients[randint(len(clients))],
            "consultant": consultants[randint(len(consultants))]}
