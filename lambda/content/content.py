import boto3
import json
import logging
from botocore.exceptions import ClientError
from content.content_interface import ContentInterface

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
TABLE_NAME = "tastingswithtay-dev-content"


def handler(event, context):
    logger.info(f"Event started: {event}")
    content_id = event["pathParameters"]["contentId"]
    logger.info(f"content_id {content_id}")
    content_interface = ContentInterface(dynamodb, TABLE_NAME)
    content_data = content_interface.get_content(content_id)
    logger.info(f"Retrieved content data: {content_data}")
    return {"statusCode": 200, "headers": {}, "body": json.dumps(content_data)}
