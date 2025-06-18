# CodeStar Connection Manually Created
# Uncomment the following lines if you want to create a new connection programmatically.
# from aws_cdk import aws_codestarconnections as codestar

# connection = codestar.CfnConnection(
#     self, "GitHubConnection",
#     connection_name="GitHubConnection", # Created in AWS CodeStar Connections
#     provider_type="GitHub"
# )
# connection_arn_value = connection.attr_connection_arn


from aws_cdk import pipelines as pipelines, aws_codebuild as codebuild, Stack, Environment
from constructs import Construct
from .lambda_stage import LambdaDeployStage


class CICDPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        conn = self.node.try_get_context("githubConnectionArn")
        source = pipelines.CodePipelineSource.connection(
            repo_string="kanitvural/20-lambda-s3-dynamodb-project",
            branch="main",
            connection_arn=conn,
        )

        synth_step = pipelines.ShellStep(
            "Synth",
            input=source,
            commands=[
                "npm install -g aws-cdk",
                "pip install -r requirements.txt",
                "cdk synth",
            ],
            # primary_output_directory="../cdk.out",
            # env={
            #     "AWS_DEFAULT_REGION": "eu-central-1",
            #     "AWS_REGION": "eu-central-1"
            # },
            # fallback default build environment
        )
        
        manual_approval = pipelines.ManualApprovalStep("ManualApproval")

        test_step = pipelines.CodeBuildStep(
            "TestStep",
            input=source,
            commands=[
                "pip install -r requirements.txt",
                "pytest tests/",
            ],
            build_environment=codebuild.BuildEnvironment(
                compute_type=codebuild.ComputeType.SMALL,
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
            ),
        )

        pipeline = pipelines.CodePipeline(self, "Pipeline", synth=synth_step)

        deploy_stage = LambdaDeployStage(self, "DeployStage", env=Environment(region="eu-central-1"))

        pipeline.add_stage(deploy_stage, pre=[manual_approval,test_step])
