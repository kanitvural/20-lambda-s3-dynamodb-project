import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("MyTable")


def lambda_handler(event, context):
    for record in event["Records"]:
        file_name = record["s3"]["object"]["key"]
        table.put_item(Item={"filename": file_name})
    return {"statusCode": 200, "body": json.dumps("Success")}
