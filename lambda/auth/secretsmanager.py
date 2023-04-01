import boto3
from botocore.exceptions import ClientError
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

session = boto3.session.Session()


def get_secret(secret_name: str, region_name: Optional[str] = "us-east-1") -> str:
    """
    Fetches the value of a secret from AWS Secrets Manager.

    Args:
        secret_name: The name of the secret to fetch.
        region_name: The AWS region where the secret is stored (default: us-east-1).

    Returns:
        The value of the secret.

    Raises:
        ClientError: If there is an error fetching the secret.
    """
    logger.info(f"Fetching token for {secret_name}")
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        logger.info(f"Was able to fetch valid token for {secret_name}")
    except ClientError as e:
        logger.error(f"Error fetching secret {secret_name}: {e}")
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response["SecretString"]

    return secret
