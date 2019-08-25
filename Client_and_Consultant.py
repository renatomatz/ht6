#creating abstract class "Person"
class person:
    name: str
    age: int
    date_of_join: str
    language: str

    def __init__(self, name:str, age: int, date_of_join: str, language:str):
        # public attributes
        self.name = name
        self.age = age
        self.date_of_join = date_of_join
        self.language = language
        # Special None case might be added later


class Client(person):
    name: str
    age: int
    income: int
    sex: str
    expenses: int
    date_of_join: str
    credit_rating: float
    intended_investment: float
    language: str
    children: int
    education: str

    def __init__(self, name: str, age: int, income: int, sex: str,\
                 expenses: str, date_of_join: str, credit_rating: float,\
                 intended_investment: float, language: str, \
                 children: int, education: str, ):
        super(person, self).__init__(name, age, date_of_join, language)
        self.income = income
        self.sex = sex
        self.expenses = expenses
        self.credit_rating = credit_rating
        self.intended_investment = intended_investment
        self.children = children
        self.education = education


class Consultant(person):
    name: str
    age: int
    experience: int
    date_of_join = str
    language = str
    client_history = list

    def __init__(self, name: str, age: int, experience: int, date_of_join: str,\
                 language: str, client_history: list):
        super(person, self).__init__(name, age, date_of_join, language)
        self.experience = experience
        self.client_history = client_history

