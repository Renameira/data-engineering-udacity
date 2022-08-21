terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.region
}

resource "aws_redshift_cluster" "redshift" {
  cluster_identifier   = var.redshify_identify
  database_name        = var.name_database
  master_username      = var.master_user_name
  master_password      = var.master_user_password
  node_type            = var.node_type_instance
  cluster_type         = var.type_cluster_instance
  publicly_accessible  = true
  enhanced_vpc_routing = true  
  skip_final_snapshot  = true
}
