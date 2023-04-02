import logging
import json
import boto3
from content.content_interface import ContentInterface

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
TABLE_NAME = "tastingswithtay-dev-content"

content_interface = ContentInterface(dynamodb, TABLE_NAME)


def handler(event, context):
    if "httpMethod" in event:
        http_method = event["httpMethod"]

        if http_method == "GET":
            try:
                path = event["pathParameters"]["contentId"]
                if path == "active":
                    content_data = content_interface.get_active_content()
                    data = content_data
                    logger.info(f"Retrieved content data: {content_data}")

                    return {
                        "statusCode": 200,
                        "headers": {},
                        "body": json.dumps(content_data),
                    }
            except KeyError as err:
                logger.error(f"Error: Missing path parameter - {err}")
                return {
                    "statusCode": 400,
                    "headers": {},
                    "body": json.dumps({"error": "Missing path parameter"}),
                }
            except Exception as err:
                logger.error(f"Error: {err}")
                return {
                    "statusCode": 500,
                    "headers": {},
                    "body": json.dumps({"error": "Internal server error"}),
                }
    else:
        return {
            "statusCode": 400,
            "headers": {},
            "body": json.dumps({"error": "Invalid request"}),
        }
