variable "region"{
  description   = "Value of the region of services"
  type          = string
  default       = "us-west-2" 
}

variable "redshify_identify" {
  description   = "Identify redshift cluster"
  type          = string
  default       = "sparkify-cluster"
}

variable "name_database" {
  description   = "Name of database in the redshift"
  type          = string
  default       = "sparkify" 
}

variable "master_user_name" {
  description   = "Name of master user"
  type          = string
  default       = "student" 
}

variable "master_user_password" {
  description   = "Name of master user"
  type          = string
  default       = "Mustbe8characters"
}

variable "node_type_instance" {
  description   = "type of instances of cluster"
  type          = string
  default       = "dc2.large"
}

variable "type_cluster_instance" {
  description   = "type of cluster"
  type          = string
  default       = "single-node"
}
