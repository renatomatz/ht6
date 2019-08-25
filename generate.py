from generators import *
import json
import os

# Create people
N_CLIENTS = 1000
N_CONSULTANTS = 100

n = 0

ages = ((0, 30), (30, 65), (65, 100))
incomes = ((0, 25000), (15000, 125000), (100000, 1000000)) 
n_transactions = ((0, 5), (3, 20), (15, 100))

for age in ages:
    for income in incomes:
        for t in n_transactions:
            for _ in range(N_CLIENTS // (len(ages)*len(incomes)*len(n_transactions))):

                cli = random_client(n, age_r=age, income_r=income, n_transactions=t)
                with open("data/clients/"+str(n)+".json", "w") as f:
                    json.dump(cli, f)

                port = random_portfolio(n, income, pd.Timestamp(cli["date_of_join"]), n_transactions=t)
                with open("data/portfolios/"+str(n)+".json", "w") as f:
                    json.dump(port, f)

                n += 1

n_clients = n

experiences = ((0, 7), (5, 15), (12, 30))

for age in ages:
    for experience in experiences:
        for t in n_transactions:
            for _ in range(N_CONSULTANTS // len(ages)*len(experiences)):

                con = random_consultant(n, age_r=age, experience_r=experience)
                with open("data/consultants/"+str(n)+".json", "w") as f:
                    json.dump(con, f)

                port = random_portfolio(n, income, pd.Timestamp(cli["date_of_join"]), n_transactions=t)
                with open("data/portfolios/"+str(n)+".json", "w") as f:
                    json.dump(port, f)

                n += 1

m = 0

for i in range(n_clients):
    
    inter = random_interaction(n, i, randint(n_clients, n_clients+n))
    with open("data/interactions/"+str(m)+".json", "w") as f:
        json.dump(inter, f)
