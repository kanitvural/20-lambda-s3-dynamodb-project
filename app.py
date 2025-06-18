# Direct Deployment of the Lambda, S3, and DynamoDB stack

# import aws_cdk as cdk
# from lambda_s3_dynamodb_stack.lambda_stack import LambdaS3DynamoDBStack

# app = cdk.App()
# region = "eu-central-1"

# LambdaS3DynamoDBStack(app, "LambdaS3DynamoDBStack", env=cdk.Environment(region=region))

# app.synth()


import aws_cdk as cdk
from lambda_s3_dynamodb_stack.pipeline_stack import CICDPipelineStack

app = cdk.App()
region = "eu-central-1"

CICDPipelineStack(app, "LambdaS3DynamoDBPipelineStack", env=cdk.Environment(region=region))

app.synth()
