output "lambda_arn" {
  value = "${aws_lambda_function.lambda_function.arn}"
}

output "lambda_iam_role_name" {
  value = "${aws_iam_role.iam_for_lambda.name}"
}

output "sns_topic_arn" {
  value = "${aws_sns_topic.topic.arn}"
}
