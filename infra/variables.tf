variable "aws_region" {
  description = "Region del laboratorio AWS Academy"
  type        = string
  default     = "us-east-1"
}

variable "student_name" {
  description = "Nombre completo del estudiante"
  type        = string
  default     = "Erick Emanuel Tamayo Diaz"
}

variable "project_name" {
  description = "Prefijo corto para los recursos"
  type        = string
  default     = "erick-dgiti"
}

variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "db_instance_class" {
  type    = string
  default = "db.t3.micro"
}
