import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    return {"statusCode": 200, "headers": {}, "body": "Hello World"}
