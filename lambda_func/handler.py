import json
import boto3

dynamodb = boto3.client("dynamodb")

TABLE_NAME = "MyTable"

def lambda_handler(event, context):
    for record in event["Records"]:
        file_name = record["s3"]["object"]["key"]
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "filename": {"S": file_name}  # string türünde olduğu belirtilmeli
            }
        )
    return {"statusCode": 200, "body": json.dumps("Success")}

