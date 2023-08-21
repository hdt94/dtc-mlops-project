variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  default = "us-east1"
  type    = string
}

variable "zone" {
  default = "us-east1-d"
  type    = string
}
