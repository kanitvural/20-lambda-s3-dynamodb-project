import json
import pytest
from lambda_func.handler import lambda_handler
from moto import mock_dynamodb
import boto3

@pytest.fixture(scope="function")
def dynamodb_table():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
        table = dynamodb.create_table(
            TableName='MyTable',
            KeySchema=[{'AttributeName': 'filename', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'filename', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
        )
        table.wait_until_exists()
        yield table

def test_lambda_handler_inserts_filename(dynamodb_table):
    mock_event = {
        "Records": [
            {"s3": {"object": {"key": "example.txt"}}}
        ]
    }
    response = lambda_handler(mock_event, {})
    assert response['statusCode'] == 200
    assert json.loads(response['body']) == 'Success'
    result = dynamodb_table.get_item(Key={"filename": "example.txt"})
    assert 'Item' in result