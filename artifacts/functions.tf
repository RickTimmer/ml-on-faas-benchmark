resource "aws_lambda_function" "lambda_function" {
  for_each = { for idx, val in local.tag_memory_combinations : "${val[0]}-${val[1]}" => val }
  
  function_name = "ml-on-faas-${each.value[0]}-${each.value[1]}MB"

  package_type = "Image"
  image_uri    = "${var.ecr_id}.dkr.ecr.eu-north-1.amazonaws.com/ml-on-faas:${each.value[0]}"

  memory_size = each.value[1]

  reserved_concurrent_executions = var.max_concurrent_executions

  role    = aws_iam_role.ml_on_faas_executor.arn
  timeout = 15
}
