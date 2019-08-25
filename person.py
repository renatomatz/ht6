#creating abstract class "Person"
from portfolio import Portfolio

class person:
    name: str
    age: int
    date_of_join: str
    language: str
    portfolio: Portfolio

    def __init__(self, name:str, age: int, date_of_join: str, language:str, \
                 portfolio=None):
        # public attributes
        self.name = name
        self.age = age
        self.date_of_join = date_of_join
        self.language = language
        self.portfolio = portfolio
        # Special None case might be added later


class Client(person):
    name: str
    age: int
    income: int
    male: bool
    expenses: int
    date_of_join: str
    credit_rating: float
    intended_investment: float
    language: str
    children: int
    education: int

    def __init__(self, name: str, age: int, income: int, male:bool,
                 expenses: str, date_of_join: str, credit_rating: float,
                 intended_investment: float, language: str, 
                 children: int, education: int, 
                 portfolio=None):

        """Initialize client

        education: int from 0-3 such that
        0 - high school incomplete
        1 - high school complete
        2 - undergraduate
        3 - graduate
        """

        super(person, self).__init__(name, age, date_of_join, language)
        self.income = income
        self.male = male
        self.expenses = expenses
        self.credit_rating = credit_rating
        self.intended_investment = intended_investment
        self.children = children
        self.education = education
        self.portfolio = portfolio


class Consultant(person):
    """
    experience: years of experience
    """

    name: str
    age: int
    experience: int
    date_of_join = str
    language = str
    client_history = list

    def __init__(self, name: str, age: int, experience: int, date_of_join: str,\
                 language: str, client_history: list, portfolio=None):

        super(person, self).__init__(name, age, date_of_join, language)
        self.experience = experience
        self.client_history = client_history
        self.portfolio = portfolio

