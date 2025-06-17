import json
import pytest
from unittest.mock import patch
import os
from lambda_func.handler import lambda_handler

@patch("lambda_func.handler.dynamodb")
def test_lambda_handler_mocked(mock_dynamodb):
    # Environment variable olarak tablo adını verelim
    os.environ["TABLE_NAME"] = "MyTable"

    mock_event = {
        "Records": [
            {"s3": {"object": {"key": "example.txt"}}}
        ]
    }

    response = lambda_handler(mock_event, {})

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == "Success"
    mock_dynamodb.put_item.assert_called_once_with(
        TableName="MyTable",
        Item={"filename": {"S": "example.txt"}}
    )

    # Test bittikten sonra ortam değişkenini temizleyebiliriz
    del os.environ["TABLE_NAME"]
