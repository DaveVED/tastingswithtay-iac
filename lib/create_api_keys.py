#!/usr/bin/env python3

import sys
from typing import Any, Dict, Optional, Union
import boto3
import secrets
import logging
import argparse
from aiohttp import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up console logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

client = boto3.client("secretsmanager", region_name="us-east-1")


class SecretsManagerSecret:
    """Encapsulates Secrets Manager functions."""

    def __init__(self, secretsmanager_client: boto3.client) -> None:
        """
        :param secretsmanager_client: A Boto3 Secrets Manager client.
        """
        self.secretsmanager_client = secretsmanager_client
        self.name: Optional[str] = None

    def _clear(self) -> None:
        """Clear the name attribute."""
        self.name = None

    def create(self, name: str, secret_value: Union[str, bytes]) -> Dict[str, Any]:
        """
        Creates a new secret. The secret value can be a string or bytes.

        :param name: The name of the secret to create.
        :param secret_value: The value of the secret.
        :return: Metadata about the newly created secret.
        """
        self._clear()
        try:
            kwargs: Dict[str, Union[str, bytes]] = {"Name": name}
            if isinstance(secret_value, str):
                kwargs["SecretString"] = secret_value
            elif isinstance(secret_value, bytes):
                kwargs["SecretBinary"] = secret_value
            response = self.secretsmanager_client.create_secret(**kwargs)
            self.name = name
            logger.info("Created secret %s.", name)
        except ClientError as e:
            logger.error(f"Error creating secret: {e}")
            raise
        else:
            return response


def generate_api_key(name: str, length: int = 64) -> str:
    """
    Generates a secure API key with the specified length.

    :param name: The name of the client.
    :param length: The length of the API key. Defaults to 64.
    :return: The generated API key.
    """
    alphabet: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    api_key: str = "".join(secrets.choice(alphabet) for i in range(length))
    return f"{name}_{api_key}"


def main() -> None:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True, help="Name of the client")
    args: argparse.Namespace = parser.parse_args()

    try:
        sm: SecretsManagerSecret = SecretsManagerSecret(client)

        api_key: str = generate_api_key(args.name)

        # Use the SecretsManagerSecret class to store the API key
        sm.create(f"{args.name}-api-key", api_key)
        logger.info(f"API key for {args.name} stored in Secrets Manager.")

    except Exception as e:
        logger.exception(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
