# AWS Lambda SNS Terraform Module

[![Build Status](https://travis-ci.org/mergermarket/tf_aws_lambda_sns.svg?branch=master)](https://travis-ci.org/mergermarket/tf_aws_lambda_sns)

This module will deploy a Lambda function and subscribe it to an SNS topic which will trigger the function.

## Module Input Variables

- `s3_bucket` - (string) - **REQUIRED** - The name of the bucket containing your uploaded Lambda deployment package.
- `s3_key` - (string) - **REQUIRED** - The s3 key for your Lambda deployment package.
- `function_name` - (string) - **REQUIRED** - The name of the Lambda function.
- `handler` - (map) - **REQUIRED** - The function within your code that Lambda calls to begin execution.
- `runtime` - (string) - **REQUIRED** The runtime environment for the Lambda function you are uploading.
- `topic_name` - (string) - **REQUIRED** The name of the SNS topic to subscribe to.
- `subnet_ids` (list) - **REQUIRED** - The ids of VPC subnets to run in.
- `security_group_ids` (list) - **REQUIRED** - The ids of VPC security groups to assign to the Lambda.
- `timeout` (string) - _optional_ - The number of seconds the Lambda will be allowed to run for.
- `lambda_env` - (string) - _optional_ - Environment parameters passed to the Lambda function.


## Usage

```hcl
module "lambda-function" {
  source                    = "github.com/mergermarket/tf_aws_lambda_sns"
  s3_bucket                 = "s3_bucket_name"
  s3_key                    = "s3_key_for_lambda"
  function_name             = "do_foo"
  handler                   = "do_foo_handler"
  runtime                   = "nodejs"
  lambda_env                = "${var.lambda_env}"
  topic_name                = "my-sns-topic"
}
```
Lambda environment variables file:
```json
{
  "lambda_env": {
    "environment_name": "ci-testing"
  }
}
```
