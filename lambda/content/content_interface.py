dave.w.dennis@gmail.com
well can we update my lambda to use the new format? 

import boto3
import logging
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from urllib.parse import urlparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ContentInterface:
    def __init__(self, dyn_resource, table_name):
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table(table_name)
        self.s3_client = boto3.client('s3', region_name="us-east-1", signatureVersion="v4")

    def get_active_content(self):
        try:
            response = self.table.query(
                IndexName="LandingActiveIndex",
                KeyConditionExpression=Key('landing').eq("true") & Key('active').eq("true")
            )
        except ClientError as err:
            logger.error(
                "Couldn't query the table %s. Here's why: %s: %s",
                self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message']
            )
            raise
        else:
            items = response.get('Items', [])
            return self._format_content_output(items)

    def _format_content_output(self, items):
        for item in items:
            # https://tastingswithtay-dev-assets.s3.amazonaws.com/dummy/beef.jpg
            image_url = item["imageUrl"]
            parsed_url = urlparse(image_url)
            bucket_name = parsed_url.netloc.split('.')[0]
            key = parsed_url.path.lstrip('/')
            presigned_url = self._generate_presigned_url(bucket_name, key, None)
            print(f"presigned url {presigned_url}")
            item["presignedUrl"] = presigned_url
        return items

    def _generate_presigned_url(self, bucket_name, object_name, expiration=None):
        if expiration is None:
            expiration = 3600 # default expiration time of 2 hours
        
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': object_name
                },
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            logging.error(e)
            return None