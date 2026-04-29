// Required Variables
variable "s3_bucket" {
  description = "The name of the bucket containing your uploaded Lambda deployment package."
}

variable "s3_key" {
  description = "The s3 key for your Lambda deployment package."
}

variable "function_name" {
  description = "The name of the Lambda function."
}

variable "handler" {
  description = "The function within your code that Lambda calls to begin execution."
}

variable "runtime" {
  description = "The runtime environment for the Lambda function you are uploading."
}

variable "topic_name" {
  description = "The name for the topic used by lambda."
}

variable "subnet_ids" {
  type        = list(string)
  description = "The VPC subnets in which the Lambda runs"
}

variable "security_group_ids" {
  type        = list(string)
  description = "The VPC security groups assigned to the Lambda"
}

variable "lambda_env" {
  description = "Environment parameters passed to the Lambda function."
  type        = map(string)
  default     = {}
}

// Optional Variables
variable "datadog_log_subscription_arn" {
  description = "Log subscription arn for shipping logs to datadog"
  default     = ""
}

variable "timeout" {
  description = "The maximum time in seconds that the Lambda can run for"
  default     = 3
}

variable "custom_sns_policy" {
  description = "Custom sns policy"
  default = null
}

variable "enable_otel_collector" {
  description = "Whether to enable the OpenTelemetry Collector Lambda Extension"
  type        = bool
  default     = false
}

variable "otel_collector_layer_extension_log_level" {
  description = "The log level for the OpenTelemetry Collector Lambda Extension"
  type        = string
  default     = "error"
}

variable "architectures" {
  description = "Instruction set architecture for the Lambda function"
  type        = list(string)
  default     = ["x86_64"]
}

variable "otel_datadog_log_subscription_arn_ssm_parameter_name" {
  description = "The SSM parameter name for the Datadog log subscription ARN used by the OpenTelemetry Collector"
  type        = string
  default     = "otel-datadog-log-subscription-role-arn"
}

variable "disable_logging" {
  description = "Whether to disable logging for the Lambda function (not recommended)"
  type        = bool
  default     = false
}