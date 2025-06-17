## Lambda‑S3‑DynamoDB — Self‑Mutating CDK Pipeline

A fully‑automated CI/CD reference project that demonstrates how to:

1. **Trigger a Lambda function** whenever a file is uploaded to an S3 bucket.
2. **Write the uploaded file name** into a DynamoDB table.
3. **Deploy everything** (S3 + Lambda + DynamoDB) via an **AWS CDK pipeline** that continuously tests, synthesises, and deploys on every GitHub push.

### Architecture

```
GitHub → CodePipeline → CodeBuild (unit tests & cdk synth)
                 │
                 └── Deploy Stage → CloudFormation → { S3 | Lambda | DynamoDB }
```

* **Self‑Mutating Pipeline** The pipeline is defined *inside* the CDK app, therefore any change to the code (new stacks, stages, etc.) automatically updates the pipeline itself.
* **CodeStar Connection** Secure GitHub connection without storing a personal access token.

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| AWS Account | Tested in `eu‑central‑1` |
| AWS CLI & CDK v2 | `npm i -g aws-cdk` |
| Python 3.11 | Project code & tests |
| GitHub Repo | Example: `kanitvural/20-lambda-s3-dynamodb-project` |

### One‑Time Setup

```bash
# 1. Clone the repo
$ git clone https://github.com/kanitvural/20-lambda-s3-dynamodb-project.git
$ cd 20-lambda-s3-dynamodb-project

# 2. Install dependencies
$ python -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt

# 3. Bootstrap the target account / region (only once)
$ cdk bootstrap aws://<ACCOUNT_ID>/eu-central-1

# 4. Deploy the pipeline stack (only once)
$ cdk deploy LambdaS3DynamoDBPipelineStack
```

> **Important:** After the first deploy, open the *AWS Console → CodeStar Connections* page and click **“Authorize”** to approve the GitHub connection.

### Development Workflow

1. **Edit code** → Implement new feature, fix a bug, or add a new stack.
2. **Commit & push** → `git push origin main`.
3. **Pipeline runs automatically**:
   * Installs dependencies.
   * Executes unit tests (`pytest`).
   * Runs `cdk synth`.
   * Deploys updated CloudFormation stacks.
4. **Observe deployments** in the CodePipeline UI or CloudFormation console.

### Local Unit Tests

Run *pytest* locally before pushing:

```bash
$ pytest tests/
```

### Clean‑up

```bash
# Destroy all CDK stacks created by the pipeline
$ cdk destroy LambdaS3DynamoDBPipelineStack

# If you need to remove the bootstrapped resources as well
$ cdk bootstrap aws://<ACCOUNT_ID>/eu-central-1 --termination
```

### Project Structure (TL;DR)

```
├── lambda/handler.py           # Lambda business logic
├── tests/                      # PyTest unit tests
├── lambda_s3_dynamodb_stack/
│   ├── lambda_stack.py         # S3 + Lambda + DynamoDB
│   ├── lambda_stage.py         # Wraps the stack into a Stage
│   └── pipeline_stack.py       # CodePipeline definition
├── app.py                      # CDK App entry point
└── README.md                   # You are here
```

Enjoy building serverless pipelines with AWS CDK! 🎉