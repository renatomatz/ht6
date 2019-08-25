from processing import *
from import_data import *

import boto3
import pandas as pd

from sagemaker import get_execution_role
from sagemaker.session import Session

from sagemaker import KMeans
from sagemaker.sklearn import SKLearn

role = get_execution_role()

bucket = "ressonance"
key = "data/training_data"
region = boto3.Session().region_name


def upload_file(f):
    boto3.Session() \
         .resource("s3", region_name=region) \
         .Bucket(bucket) \
         .Object(key) \
         .upload_file(f)


## Step 1: portfolio

ports = None
ports_df = portfolio_processing(ports)
ports_df.to_csv(key+"portfolios.csv")
upload_file(key+"portfolios.csv")

s3_client = boto3.client("s3")

data_path = "s3://ressonance/data/model_data/"
output_path = "s3://ressonance/models/"

# portfolio clustering

port_kmeans = KMeans(role=role,
                     train_instance_count=2,
                     train_instance_type="ml.c4.xlarge",
                     output_path=output_path+"portfolio",
                     k=5,
                     data_location=data_path+"portfolios.csv")

port_training = pd.read_csv("data/training_data/portfolios.csv")

port_kmeans.fit(port_kmeans.record_set(port_training))
port_predictor = port_kmeans.deploy(initial_instance_count=1,
                                    instance_type="ml.m4.xlarge")

## Step 2: people 
# Substiuting portfolios


def sub_port(port):
    return port_predictor(portfolio_processing(list(port)))


clis = None
clis_df = client_processing(clis)

clis_df.portfolio = sub_port(clis_df.portfolio)

clis_df.to_csv(key+"clients.csv")

upload_file(key+"clients.csv")

cons = None
cons_df = consultant_processing(cons)

cons_df.portfolio = sub_port(cons_df.portfolio)
cons_df.to_csv(key+"consultants.csv")

upload_file(key+"consultants.csv")

# consultant clustering

cons_kmeans = KMeans(role=role,
                     train_instance_count=2,
                     train_instance_type="ml.c4.xlarge",
                     output_path=output_path+"consultant",
                     k=5,
                     data_location=data_path+"consultants.csv")

cons_kmeans.fit(cons_kmeans.record_set(cons_df))
cons_predictor = cons_kmeans.deploy(initial_instance_count=1,
                                    instance_type="ml.m4.xlarge")

## Building matcher
# interaction formatting

inters = None
inters_df = interaction_processing(inters)

inters_df.client.portfolio = sub_port(client_processing( \
                                        list(inters_df.client)).portfolio)

inters_df.consultant.portfolio = sub_port(consultant_processing( \
                                            list(inters_df.consultant)).portfolio)

inters_df.consultant = cons_predictor(consultant_processing( \
                                        list(inters_df.consultant)))

inters_df = pd.concat([inters_df.drop(["client", 
                                       "duration", 
                                       "ongoing", 
                                       "n_transactions"], axis=1), 
                       client_processing(list(inters_df.client))], axis=1)

inters_df.to_csv(key+"interactions.csv")

upload_file(key+"interactions.csv")

models = {}

for name, df in inters_df.groupby("consultant"):
    
    model = SKLearn(entry_point="training_scripts.py",
                    train_instance_type="ml.c4.xlarge",
                    role=role,
                    sagemaker_session=sagemaker_session,
                    hyperparameters={"normalize": True})

    model_fit = model.fit({"train": df})
    models[name] = model_fit.deploy(initial_instance_count=1,
                                    instance_type="ml.m4.xlarge")



