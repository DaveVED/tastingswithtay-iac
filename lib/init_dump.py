#!/usr/bin/env python3

import boto3

BUCKET_NAME = "tastingswithtay-dev-assets"

client = boto3.client("s3", region_name="us-east-1")


def main():
    print("HI")


if __name__ == "__main__":
    main()
