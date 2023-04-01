#!/usr/bin/env python3
import os
import json
import boto3
import uuid
import datetime
import logging

AWS_REGION = "us-east-1"
BUCKET_NAME = "tastingswithtay-dev-assets"
TABLE_NAME = "tastingswithtay-dev-content"

s3 = boto3.client("s3", region_name=AWS_REGION)

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_init_data() -> list:
    """
    Load initial data from JSON file.

    Returns:
        A list of dictionaries representing the data.
    """
    logger.info("Loading initial data...")
    with open(os.path.join(dir_path, "scripts/init.json")) as f:
        data = json.load(f)
    logger.info(f"Loaded {len(data)} items from JSON file.")
    return data


def upload_files_to_s3(data: list) -> dict:
    """
    Upload files to S3 and update their URLs in the content data.

    Args:
        data: A list of dictionaries representing the content data.

    Returns:
        A dictionary of file URLs, with keys being image names.

    Raises:
        Exception: If there is an error uploading a file to S3.
    """
    logger.info("Uploading files to S3...")
    content_dict = {content["contentName"]: content for content in data}
    file_urls = {}
    for file in os.listdir(f"{dir_path}/assets/dummy"):
        image_name, image_type = file.split(".")
        content = content_dict.get(image_name)
        if content:
            with open(os.path.join(dir_path, "assets/dummy", file), "rb") as f:
                file_content = f.read()
            key = f"dummy/{file}"
            try:
                response = s3.put_object(Body=file_content, Bucket=BUCKET_NAME, Key=key)
            except Exception as e:
                logger.error(
                    f"Failed to upload file {key} to S3 bucket {BUCKET_NAME}: {e}"
                )
                raise e
            file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
            logger.info(f"Uploaded file {key} to S3 bucket {BUCKET_NAME}")
            content["imageUrl"] = file_url
            file_urls[image_name] = file_url
    logger.info(f"Uploaded {len(file_urls)} files to S3.")
    return file_urls


def write_to_dynamodb(data: list) -> None:
    """
    Write content data to DynamoDB.

    Args:
        data: A list of dictionaries representing the content data.

    Raises:
        Exception: If there is an error writing to DynamoDB.
    """
    logger.info("Writing data to DynamoDB...")
    for content in data:
        try:
            content_id = str(uuid.uuid4())
            sort_key = content["contentName"]
            current_time = str(datetime.datetime.utcnow().isoformat())
            table.put_item(
                Item={
                    "contentId": content_id,
                    "sortKey": sort_key,
                    "contentType": content["contentType"],
                    "shortDescription": content["shortDescription"],
                    "landing": content["landing"],
                    "imageUrl": content["imageUrl"],
                    "active": content["active"],
                    "createdBy": "init",
                    "createdOn": current_time,
                }
            )
            logger.info(
                f"Wrote item with contentId {content_id} and sortKey {sort_key} to DynamoDB table {TABLE_NAME}"
            )
        except Exception as e:
            logger.error(
                f"Failed to write item with contentName {sort_key} to DynamoDB table {TABLE_NAME}: {e}"
            )
            raise e


def main() -> None:
    """
    Main function to load initial data, upload files to S3, and write data to DynamoDB.
    """
    try:
        data = load_init_data()
        logger.info(f"Loaded {len(data)} items of initial data.")
        file_urls = upload_files_to_s3(data)
        write_to_dynamodb(data)
        logger.info(
            "Successfully loaded initial data, uploaded files to S3, and wrote data to DynamoDB."
        )
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise e


if __name__ == "__main__":
    main()
