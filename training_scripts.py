import argparse
import os

import numpy as np
from sklearn.linear_model import LinearRegression

if __name__ == '__from sagemaker import KMeans

main__':
    
    parser = argparse.ArgumentParser()

    # hyperparameters 
    parser.add_argument("--normalize", type=bool, default=True)

    #sagemaker params
    parser.add_argument("--output-data-dir", 
                        type=str, 
                        default=os.environ["SM_OUTPUT_DATA_DIR"])

    parser.add_argument("--model-dir", 
                        type=str,
                        default=os.environ["SM_MODEL_DIR"])

    parser.add_argument("--train",
                        type=str,
                        default=os.environ["SM_CHANNEL_TRAIN"])

    args = parser.parse_args()

    df = args.train

    y = np.array(df.score)
    X = np.array(df.drop("score", "consultant"))

    models = LinearRegression(normalize=args.normalize).fit(X, y)

    joblib.dump(models, 
                os.path.join(args.model_dir, 
                             "interaction_model" + \
                                str(df.consultant[0]) + \
                                ".joblib"))
        
