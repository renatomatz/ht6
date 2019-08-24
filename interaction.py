from typing import Unite
from datetime import date

import pandas as pd
from person import Client, Consultant

class Interaction:
    """
    """

    client: Client
    consultant: Consultant
    start: pd.Timestamp
    end: Unite[pd.Timestamp, None]

    def __init__(self, client, consultant, start):

        self.client = client
        self.consultant = consultant
        self.start = start
        self.end = None

    def terminate(self, time):
        self.end = time

    def inter_days(self):
        if self.end:
            end = self.end
        else:
            end = pd.Timestamp(date.today())

        td = end - self.start
        return td.days

    def interaction_returns(self):
        return self.client.portfolio.get_returns(annualized_latest=False, \
                                                 self.start, self.end)

    def transactions(self):

        t = self.client.portfolio.history.copy()
        t = t[t.index >= self.start]
        
        if self.end:
            t = t[t.index <= self.end]

        return t

    def n_transactions(self):
        return len(self.transactions)

    def ammount_invested(self, rel_to_income=True):
        total = self.transactions.iloc[0].sum()

        return total / self.client.income if rel_to_income else total