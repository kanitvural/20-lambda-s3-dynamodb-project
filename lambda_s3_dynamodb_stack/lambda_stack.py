from aws_cdk import (
    Stack, aws_lambda as _lambda, aws_dynamodb as dynamodb,
    aws_s3 as s3, aws_s3_notifications as s3n,
    aws_iam as iam, Duration, Size
)
from constructs import Construct

class LambdaS3DynamoDBStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "MyBucket")

        table = dynamodb.Table(
            self, "MyTable",
            partition_key={"name": "filename", "type": dynamodb.AttributeType.STRING},
            read_capacity=1, write_capacity=1
        )

        lambda_role = iam.Role(
            self, "LambdaDynamoDBRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["dynamodb:PutItem"],
            resources=[table.table_arn]
        ))

        fn = _lambda.Function(
            self, "MyFunction",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(10),
            memory_size=256,
            ephemeral_storage_size=Size.mebibytes(512),
            role=lambda_role
        )

        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, s3n.LambdaDestination(fn))

        fn.add_permission("AllowS3Invoke",
            principal=iam.ServicePrincipal("s3.amazonaws.com"),
            source_arn=bucket.bucket_arn)