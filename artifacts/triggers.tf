resource "aws_sns_topic" "ml_on_faas_sns" {
  name = "ml-on-faas-sns-topic"
}

resource "aws_sns_topic_subscription" "lambda_sns_subscription" {
  for_each = { for idx, val in local.tag_memory_combinations : "${val[0]}-${val[1]}" => val }

  topic_arn = aws_sns_topic.ml_on_faas_sns.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.lambda_function["${each.value[0]}-${each.value[1]}"].arn
}

resource "aws_lambda_permission" "with_sns" {
  for_each = { for idx, val in local.tag_memory_combinations : "${val[0]}-${val[1]}" => val }

  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function["${each.value[0]}-${each.value[1]}"].function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.ml_on_faas_sns.arn
}
