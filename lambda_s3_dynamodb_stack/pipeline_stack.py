from aws_cdk import pipelines as pipelines
from aws_cdk import Stack, Environment, aws_codestarconnections as codestar
from constructs import Construct
from .lambda_stage import LambdaDeployStage

class CICDPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        connection = codestar.CfnConnection(
            self, "GitHubConnection",
            connection_name="GitHubConnection",
            provider_type="GitHub"
        )

        pipeline = pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection(
                    repo_string="kanitvural/20-lambda-s3-dynamodb-project",
                    branch="main",
                    connection_arn=connection.attr_connection_arn
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "pytest",
                    "cdk synth"
                ]
            )
        )

        deploy_stage = LambdaDeployStage(self, "DeployStage", env=Environment(region="eu-central-1"))
        pipeline.add_stage(deploy_stage)