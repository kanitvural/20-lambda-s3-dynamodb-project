import os
import json
import boto3

dynamodb = boto3.client("dynamodb")

def lambda_handler(event, context):
    
    TABLE_NAME = os.getenv("TABLE_NAME", None)
    
    for record in event["Records"]:
        file_name = record["s3"]["object"]["key"]
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item={
                "filename": {"S": file_name} 
            }
        )
        
    return {"statusCode": 200, "body": json.dumps("Success")}

