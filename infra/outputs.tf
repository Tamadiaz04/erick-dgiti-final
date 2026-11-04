output "application_url" {
  description = "URL publica del servicio"
  value       = "http://${aws_lb.app.dns_name}"
}

output "health_url" {
  description = "Endpoint de validacion"
  value       = "http://${aws_lb.app.dns_name}/health"
}

output "api_test_url" {
  value = "http://${aws_lb.app.dns_name}/api/test"
}

output "load_balancer_dns" {
  value = aws_lb.app.dns_name
}

output "autoscaling_group" {
  value = aws_autoscaling_group.app.name
}

output "database_primary_endpoint" {
  value = aws_db_instance.primary.address
}

output "database_replica_endpoint" {
  value = aws_db_instance.replica.address
}

output "database_security_group" {
  value = aws_security_group.database.id
}

output "cloudwatch_dashboard" {
  value = aws_cloudwatch_dashboard.main.dashboard_name
}
