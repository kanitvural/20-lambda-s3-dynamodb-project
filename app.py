import aws_cdk as cdk
from lambda_s3_dynamodb_stack.pipeline_stack import CICDPipelineStack

app = cdk.App()
region = "eu-central-1"

CICDPipelineStack(app, "LambdaS3DynamoDBPipelineStack", env=cdk.Environment(region=region))

app.synth()
