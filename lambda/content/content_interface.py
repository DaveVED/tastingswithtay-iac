class ContentInterface:
    def __init__(self, dyn_resource, table_name):
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table(table_name)

    def get_content(self, content_id):
        try:
            response = self.table.get_item(Key={"contentId": content_id})
        except ClientError as err:
            logger.error(
                "Couldn't get content with contentId %s from table %s. Here's why: %s: %s",
                content_id,
                self.table.name,
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
        else:
            return response.get("Item")
