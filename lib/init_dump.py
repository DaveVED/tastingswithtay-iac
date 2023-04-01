#!/usr/bin/env python3

import os
import json
import boto3

BUCKET_NAME = "tastingswithtay-dev-assets"

client = boto3.client("s3", region_name="us-east-1")


def load_init_data():
    data = None
    with open(os.path.join(os.path.dirname(__file__), "init.json")) as f:
        data = json.load(f)
    return data


def populate_init_data(data):
    for input in data:
        print(input)


def main():
    data = load_init_data()
    populate_init_data(data)


if __name__ == "__main__":
    main()
