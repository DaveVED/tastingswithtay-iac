import logging
from typing import List, Dict
from auth import secretsmanager as sm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def validate_token_formatting(token_criteria: List[str]) -> bool:
    """
    Check if the authorization token has the expected format.

    Args:
        token_criteria: A list of two elements, where the second element is the authorization token.

    Returns:
        True if the token has the expected format, False otherwise.
    """
    if len(token_criteria) != 2:
        logger.error("Formatting error for authorizationToken.")
        return False

    token = token_criteria[1]

    if len(token) == 64:
        logger.info(f"authorizationToken ending with {token[-4:]} provided.")
        return True

    logger.error("Invalid token length provided.")
    return False


def validate_token(client: str, token: str) -> bool:
    """
    Check if the provided client and token are valid.

    Args:
        client: The client name.
        token: The authorization token.

    Returns:
        True if the client and token are valid, False otherwise.
    """
    formatted_client = f"{client}-api-key"
    valid_token = sm.get_secret(formatted_client, "us-east-1")
    valid_client, valid_token = valid_token.split("_")

    if client == valid_client and token == valid_token:
        return True

    return False


def generate_policy(principal_id: str, effect: str, event: Dict) -> Dict:
    """
    Generate the policy document based on the provided principal, effect, and event.

    Args:
        principal_id: The principal ID.
        effect: The policy effect ("Allow" or "Deny").
        event: The API Gateway event.

    Returns:
        A dictionary containing the generated policy.
    """
    method_arn = event["methodArn"]
    api_gateway_arn = method_arn.split(":")
    aws_account_id = api_gateway_arn[4]
    api_region = api_gateway_arn[3]
    api_id = api_gateway_arn[5].split("/")[0]
    api_stage = api_gateway_arn[5].split("/")[1]

    policy = {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": [
                        f"arn:aws:execute-api:{api_region}:{aws_account_id}:{api_id}/{api_stage}/*/*"
                    ],
                }
            ],
        },
    }

    return policy
