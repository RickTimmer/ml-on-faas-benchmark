resource "aws_iam_role" "ml_on_faas_executor" {
  name = "ml_on_faas_executor"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "ml_on_faas_policy" {
  name        = "ml_on_faas_policy"
  description = "IAM policy for logging from a lambda"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ml_on_faas_logs" {
  role       = aws_iam_role.ml_on_faas_executor.name
  policy_arn = aws_iam_policy.ml_on_faas_policy.arn
}

resource "aws_iam_role" "ml_on_faas_experiments_executor_role" {
  name               = "ml-on-faas-experiments-executor-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ml_on_faas_experiments_attachment_ecs" {
  role       = aws_iam_role.ml_on_faas_experiments_executor_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "ml_on_faas_experiments_role" {
  name               = "ml-on-faas-experiments-role"
  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ml_on_faas_experiments_attachment_sns" {
  role       = aws_iam_role.ml_on_faas_experiments_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}

resource "aws_iam_role_policy_attachment" "ml_on_faas_experiments_attachment_s3_read" {
  role       = aws_iam_role.ml_on_faas_experiments_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
}
