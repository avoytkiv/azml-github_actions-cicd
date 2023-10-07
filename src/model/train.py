# Import libraries

import argparse
import glob
import os

import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import mlflow
from mlflow.models import infer_signature


import sys

# Get the current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory
parent_dir = os.path.dirname(os.path.dirname(current_dir))
# Add the root directory to the python path
sys.path.append(parent_dir)


def main(args):

    # TO DO: enable autologging
    mlflow.sklearn.autolog(log_models=False)

    # read data
    df = get_csvs_df(args.training_data)

    # split data
    # Seperate features and target
    df_features = df.drop("Diabetic", axis=1)
    df_target = df["Diabetic"]
    X_train, X_test, y_train, y_test = train_test_split(df_features,
                                                        df_target,
                                                        test_size=0.2,
                                                        random_state=42)

    # train model
    model = train_model(args.reg_rate, X_train, y_train)

    # Signature
    signature = infer_signature(X_test, y_test)

    # Sample
    input_example = X_train.sample(n=1)

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        conda_env="conda_env.yml",
        signature=signature,
        input_example=input_example
    )


def get_csvs_df(path):
    # path = parent_dir + "/" + path
    if not os.path.exists(path):
        raise RuntimeError(f"Cannot use non-existent path provided: {path}")
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise RuntimeError(f"No CSV files found in provided data path: {path}")
    return pd.concat((pd.read_csv(f) for f in csv_files), sort=False)


# TO DO: add function to split data


def train_model(reg_rate, X_train, y_train):
    # train model
    model = LogisticRegression(C=1/reg_rate, solver="liblinear")
    model.fit(X_train, y_train)
    return model


def parse_args():
    # setup arg parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument("--training_data", dest='training_data',
                        type=str, default="experimentation/data/")
    parser.add_argument("--reg_rate", dest='reg_rate',
                        type=float, default=0.01)

    # parse args
    args = parser.parse_args()

    # return args
    return args


if __name__ == "__main__":
    # add space in logs
    print("\n\n")
    print("*" * 60)

    # parse args
    args = parse_args()

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")
