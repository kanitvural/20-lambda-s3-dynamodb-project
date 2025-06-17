import json
import pytest
from unittest.mock import patch
from lambda_func.handler import lambda_handler

@patch("lambda_func.handler.dynamodb")
def test_lambda_handler_mocked(mock_dynamodb):
    mock_event = {
        "Records": [
            {"s3": {"object": {"key": "example.txt"}}}
        ]
    }

    # put_item fonksiyonu çağrıldı mı diye kontrol edelim
    response = lambda_handler(mock_event, {})

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == "Success"
    mock_dynamodb.put_item.assert_called_once_with(
        TableName="MyTable",
        Item={"filename": {"S": "example.txt"}}
    )
