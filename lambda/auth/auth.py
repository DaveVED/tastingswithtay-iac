import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def generate_policy(principal_id, effect, resource):
    return {
        "principalId": principal_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "*",
                    "Effect": effect,
                    "Resource": resource,
                }
            ],
        },
    }


def handler(event, context):
    principal_id = "*"
    effect = "Allow"
    resource = "*"

    return generate_policy(principal_id, effect, resource)
