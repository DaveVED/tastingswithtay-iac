import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(f" EVENT: {event}")
    logger.info(f"EVENT2")
    return {"statusCode": 200, "Body": "Hello World"}
