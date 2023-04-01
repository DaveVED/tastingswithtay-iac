#!/usr/bin/env python3

import os
import json
import boto3

dir_path = os.path.dirname(os.path.realpath(__file__))

BUCKET_NAME = "tastingswithtay-dev-assets"

client = boto3.client("s3", region_name="us-east-1")


def load_init_data():
    data = None
    with open(os.path.join(os.path.dirname(__file__), "init.json")) as f:
        data = json.load(f)
    return data


def populate_init_data(data):
    for file in os.listdir(f"{dir_path}/assests/dummy"):
        print(file)


def main():
    data = load_init_data()
    populate_init_data(data)


if __name__ == "__main__":
    main()
