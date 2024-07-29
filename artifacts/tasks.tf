resource "aws_ecs_cluster" "ml_on_faas_cluster" {
  name = "ml-on-faas-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_ecs_cluster_capacity_providers" "ml_on_faas_cluster_capacity_provider" {
  cluster_name = aws_ecs_cluster.ml_on_faas_cluster.name

  capacity_providers = ["FARGATE"]

  default_capacity_provider_strategy {
    capacity_provider = "FARGATE"
    base = 0
    weight = 1
  }
}

resource "aws_ecs_task_definition" "my_task_definition" {
  family                   = "ml-on-faas-cluster-experiments-task"
  requires_compatibilities = ["FARGATE"]
  cpu = 256
  memory = 512
  task_role_arn = aws_iam_role.ml_on_faas_experiments_role.arn
  execution_role_arn = aws_iam_role.ml_on_faas_experiments_executor_role.arn
  network_mode = "awsvpc"

  container_definitions   = <<DEFINITION
[
  {
    "name": "experiments",
    "image": "${var.ecr_id}.dkr.ecr.eu-north-1.amazonaws.com/ml-on-faas:experiments",
    "cpu": 256,
    "memory": 512,
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "ml-on-faas-experiments-log-group",
        "awslogs-region": "${var.aws_region}",
        "awslogs-stream-prefix": "ml-on-faas-experimeriments"
      }
    },
    "environment": [
        {
          "name": "BATCH_SIZES",
          "value": "${var.batch_sizes}"
        },
        {
          "name": "MAX_MESSAGES",
          "value": "${var.max_messages}"
        },
        {
          "name": "DATASET_KEY",
          "value": "${var.dataset_key}"
        }
      ]
  }
]
DEFINITION
}

resource "aws_cloudwatch_log_group" "ml_on_faas_experiments_log_group" {
  name = "ml-on-faas-experiments-log-group"
}
