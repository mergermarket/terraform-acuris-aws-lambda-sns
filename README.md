# AWS Lambda SNS Terraform Module

[![Test](https://github.com/mergermarket/terraform-acuris-aws-lambda-sns/actions/workflows/test.yml/badge.svg)](https://github.com/mergermarket/terraform-acuris-aws-lambda-sns/actions/workflows/test.yml)

This module will deploy a Lambda function and subscribe it to an SNS topic which will trigger the function.

## Module Input Variables

### Required

- `s3_bucket` - (string) - The name of the bucket containing your uploaded Lambda deployment package.
- `s3_key` - (string) - The s3 key for your Lambda deployment package.
- `function_name` - (string) - The name of the Lambda function.
- `handler` - (string) - The function within your code that Lambda calls to begin execution.
- `runtime` - (string) - The runtime environment for the Lambda function you are uploading.
- `topic_name` - (string) - The name of the SNS topic to subscribe to.
- `subnet_ids` - (list(string)) - The VPC subnets in which the Lambda runs.
- `security_group_ids` - (list(string)) - The VPC security groups assigned to the Lambda.

### Optional

- `lambda_env` - (map(string)) - Environment parameters passed to the Lambda function. Default: `{}`.
- `timeout` - (number) - The maximum time in seconds that the Lambda can run for. Default: `3`.
- `datadog_log_subscription_arn` - (string) - Log subscription ARN for shipping logs to Datadog. Default: `""`.
- `custom_sns_policy` - (string) - Custom SNS policy. Default: `null`.
- `enable_otel_collector` - (bool) - Whether to enable the OpenTelemetry Collector Lambda Extension. Default: `false`.
- `otel_collector_layer_extension_log_level` - (string) - The log level for the OpenTelemetry Collector Lambda Extension. Default: `"error"`.
- `architectures` - (list(string)) - Instruction set architecture for the Lambda function. Default: `["x86_64"]`.
- `otel_datadog_log_subscription_arn_ssm_parameter_name` - (string) - The SSM parameter name for the Datadog log subscription ARN used by the OpenTelemetry Collector. Default: `"otel-datadog-log-subscription-role-arn"`.

## Outputs

- `lambda_arn` - The ARN of the Lambda function.
- `lambda_iam_role_name` - The name of the IAM role used by the Lambda function.
- `sns_topic_arn` - The ARN of the SNS topic.

## Usage

```hcl
module "lambda-function" {
  source             = "mergermarket/aws-lambda-sns/acuris"
  version            = "0.0.1"
  s3_bucket          = "s3_bucket_name"
  s3_key             = "s3_key_for_lambda"
  function_name      = "do_foo"
  handler            = "do_foo_handler"
  runtime            = "nodejs"
  lambda_env         = var.lambda_env
  topic_name         = "my-sns-topic"
  subnet_ids         = var.subnet_ids
  security_group_ids = var.security_group_ids
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
