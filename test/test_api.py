#!/usr/bin/env python3
import requests
import boto3
from botocore.exceptions import ClientError
from typing import Optional


session = boto3.session.Session()


def get_secret(secret_name: str, region_name: Optional[str] = "us-east-1") -> str:
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error fetching secret {secret_name}: {e}")
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]

    return secret


def main():
    # Replace with your actual access token
    access_token = get_secret("tastingswithtay-api-key", "us-east-1")

    # Construct the request headers with the Authorization header
    headers = {"Authorization": access_token, "client_id": "tastingswithtay"}

    response = requests.get(
        "https://dev-api.tastingswithtay.com/v1/content/active",
        headers=headers,
    )
    # Make the API request
    # response = requests.get(
    #    "https://dev-api.tastingswithtay.com/v1/content/9f22ea12-c858-4bca-832e-cd477aa61e6e",
    #    headers=headers,
    # )
    print(response.text)


if __name__ == "__main__":
    main()
