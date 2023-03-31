#!/usr/bin/env python3

import sys
import boto3
import secrets
import logging
import argparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client("secretsmanager", region_name="us-east-1")


def generate_api_key(client: str, length=64) -> str:
    """Generate a secure API key with the specified length."""
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    api_key = "".join(secrets.choice(alphabet) for i in range(length))
    return f"{client}_{api_key}"


def create_secert(api_key: str):
    try:
        pass
    except Exception as e:
        logger.error(f"error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client", required=True, help="Name of the client")
    args = parser.parse_args()

    try:
        api_key = generate_api_key(args.client)
        create_secert(api_key)
    except Exception as e:
        logger.info(f"error {e}")
        sys.exit(0)


if __name__ == "__main__":
    main()
