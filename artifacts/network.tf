data "aws_vpc" "default" {
  default = true
}

data "aws_security_group" "default_security_group" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

  filter {
    name   = "group-name"
    values = ["default"]
  }
}

data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

output "default_security_group_id" {
  value = data.aws_security_group.default_security_group.id
}

output "default_subnet_ids" {
  value = data.aws_subnets.default_subnets.ids
}
