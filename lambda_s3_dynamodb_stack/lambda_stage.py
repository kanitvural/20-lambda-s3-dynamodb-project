from aws_cdk import Stage
from constructs import Construct
from .lambda_stack import LambdaS3DynamoDBStack

class LambdaDeployStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        LambdaS3DynamoDBStack(self, "LambdaStack")