import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f"event started {event}")
    return {"statusCode": 200, "headers": {}, "body": "Hello World"}
