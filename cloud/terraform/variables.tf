variable "project_id" { type = string }
variable "region" { type = string }
variable "zone" { type = string }
variable "cluster_name" { type = string  default = "cognira-bti-gke" }
variable "artifact_repo" { type = string  default = "cognira-bti" }
variable "environment" { type = string  default = "hackathon" }
variable "gke_node_machine_type" { type = string default = "e2-standard-4" }
variable "gke_min_nodes" { type = number default = 1 }
variable "gke_max_nodes" { type = number default = 3 }
variable "ethereum_rpc_machine_type" { type = string default = "e2-standard-4" }
variable "ethereum_rpc_disk_gb" { type = number default = 200 }
variable "network_name" { type = string default = "cognira-bti-vpc" }
variable "subnet_cidr" { type = string default = "10.40.0.0/20" }
variable "pods_cidr" { type = string default = "10.44.0.0/14" }
variable "services_cidr" { type = string default = "10.48.0.0/20" }
variable "gcul_endpoint" { type = string default = "" }
variable "gcul_chain_id" { type = string default = "gcul-hackathon" }
variable "gcul_secret_password" { type = string sensitive = true default = null }
variable "ethereum_rpc_password" { type = string sensitive = true default = null }
variable "app_admin_password" { type = string sensitive = true default = null }
