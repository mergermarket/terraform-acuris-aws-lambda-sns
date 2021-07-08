import unittest
from textwrap import dedent
from subprocess import check_call, check_output
class TestLambda(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'init', 'test/infra'])

    def test_all_resources_to_be_created(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert dedent("""
            Plan: 6 to add, 0 to change, 0 to destroy.
        """).strip() in output

    def test_create_lambda(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert """
  # module.lambda.aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + arn                            = (known after apply)
      + function_name                  = "check_lambda_function"
      + handler                        = "some_handler"
      + id                             = (known after apply)
      + invoke_arn                     = (known after apply)
      + last_modified                  = (known after apply)
      + memory_size                    = 128
      + package_type                   = "Zip"
      + publish                        = false
      + qualified_arn                  = (known after apply)
      + reserved_concurrent_executions = -1
      + role                           = (known after apply)
      + runtime                        = "python2.7"
      + s3_bucket                      = "cdflow-lambda-releases"
      + s3_key                         = "s3key.zip"
      + signing_job_arn                = (known after apply)
      + signing_profile_version_arn    = (known after apply)
      + source_code_hash               = (known after apply)
      + source_code_size               = (known after apply)
      + timeout                        = 3
      + version                        = (known after apply)

      + environment {}

      + tracing_config {
          + mode = (known after apply)
        }

      + vpc_config {
          + vpc_id = (known after apply)
        }
    }
        """.strip() in output

    def test_create_lambda_in_vpc(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'subnet_ids=[1,2,3]',
            '-var', 'security_group_ids=[4]',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert """
  # module.lambda.aws_lambda_function.lambda_function will be created
  + resource "aws_lambda_function" "lambda_function" {
      + arn                            = (known after apply)
      + function_name                  = "check_lambda_function"
      + handler                        = "some_handler"
      + id                             = (known after apply)
      + invoke_arn                     = (known after apply)
      + last_modified                  = (known after apply)
      + memory_size                    = 128
      + package_type                   = "Zip"
      + publish                        = false
      + qualified_arn                  = (known after apply)
      + reserved_concurrent_executions = -1
      + role                           = (known after apply)
      + runtime                        = "python2.7"
      + s3_bucket                      = "cdflow-lambda-releases"
      + s3_key                         = "s3key.zip"
      + signing_job_arn                = (known after apply)
      + signing_profile_version_arn    = (known after apply)
      + source_code_hash               = (known after apply)
      + source_code_size               = (known after apply)
      + timeout                        = 3
      + version                        = (known after apply)

      + environment {}

      + tracing_config {
          + mode = (known after apply)
        }

      + vpc_config {
          + security_group_ids = [
              + "4",
            ]
          + subnet_ids         = [
              + "1",
              + "2",
              + "3",
            ]
          + vpc_id             = (known after apply)
        }
    }
        """.strip() in output

    def test_lambda_in_vpc_gets_correct_execution_role(self):
        output = check_output([
            'terraform',
            'plan',
            '-var', 'subnet_ids=[1,2,3]',
            '-var', 'security_group_ids=[4]',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert """
  # module.lambda.aws_iam_role_policy_attachment.vpc_permissions[0] will be created
  + resource "aws_iam_role_policy_attachment" "vpc_permissions" {
      + id         = (known after apply)
      + policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
      + role       = (known after apply)
    }
        """.strip() in output

    def test_sns_topic_created(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert """
  # module.lambda.aws_sns_topic.topic will be created
  + resource "aws_sns_topic" "topic" {
      + arn                         = (known after apply)
      + content_based_deduplication = false
      + fifo_topic                  = false
      + id                          = (known after apply)
      + name                        = "my-topic"
      + name_prefix                 = (known after apply)
      + policy                      = (known after apply)
    }
        """.strip() in output

    def test_sns_topic_subscription_created(self):
        output = check_output([
            'terraform',
            'plan',
            '-no-color',
            '-target=module.lambda',
            'test/infra'
        ]).decode('utf-8')
        assert """
  + resource "aws_sns_topic_subscription" "topic_lambda" {
      + arn                             = (known after apply)
      + confirmation_timeout_in_minutes = 1
      + confirmation_was_authenticated  = (known after apply)
      + endpoint                        = (known after apply)
      + endpoint_auto_confirms          = false
      + id                              = (known after apply)
      + owner_id                        = (known after apply)
      + pending_confirmation            = (known after apply)
      + protocol                        = "lambda"
      + raw_message_delivery            = false
      + topic_arn                       = (known after apply)
    }
        """.strip() in output
