resource "aws_lambda_function" "lambda_function" {
  s3_bucket     = "${var.s3_bucket}"
  s3_key        = "${var.s3_key}"
  function_name = "${var.function_name}"
  role          = "${aws_iam_role.iam_for_lambda.arn}"
  handler       = "${var.handler}"
  runtime       = "${var.runtime}"
  timeout       = "${var.timeout}"

  vpc_config {
    subnet_ids         = "${var.subnet_ids}"
    security_group_ids = ["${var.security_group_ids}"]
  }

  environment {
    variables = "${var.lambda_env}"
  }
}

resource "aws_sns_topic" "topic" {
  name = "${var.topic_name}"
}

resource "aws_sns_topic_subscription" "topic_lambda" {
  topic_arn = "${aws_sns_topic.topic.arn}"
  protocol  = "lambda"
  endpoint  = "${aws_lambda_function.lambda_function.arn}"
}

resource "aws_lambda_permission" "with_sns" {
    statement_id = "AllowExecutionFromSNS"
    action = "lambda:InvokeFunction"
    function_name = "${aws_lambda_function.lambda_function.arn}"
    principal = "sns.amazonaws.com"
    source_arn = "${aws_sns_topic.topic.arn}"
}

resource "aws_cloudwatch_log_group" "lambda_loggroup" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 7
  depends_on      = ["aws_lambda_function.lambda_function"]

}


resource "aws_cloudwatch_log_subscription_filter" "kinesis_log_stream" {
  count           = "${var.datadog_log_subscription_arn != "" ? 1 : 0}"
  name            = "kinesis-log-stream-${var.function_name}"
  destination_arn = "${var.datadog_log_subscription_arn}"
  log_group_name  = "${aws_cloudwatch_log_group.lambda_loggroup.name}"
  filter_pattern  = ""
  depends_on      = ["aws_cloudwatch_log_group.lambda_loggroup"]
}
