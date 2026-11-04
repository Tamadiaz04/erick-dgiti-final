# Evaluacion final DGITI - Erick Emanuel Tamayo Diaz

Proyecto demostrativo para desplegar en AWS una aplicacion altamente disponible,
una base de datos PostgreSQL con replica, controles de red, monitoreo y pruebas.

## Arquitectura

- VPC propia en dos zonas de disponibilidad.
- Application Load Balancer publico.
- Auto Scaling Group con dos instancias EC2 privadas (maximo cuatro).
- Amazon RDS for PostgreSQL primario y replica de lectura en subredes privadas.
- Security Groups encadenados: Internet -> ALB -> aplicacion -> RDS.
- Dashboard de CloudWatch con solicitudes, errores, latencia, targets y CPU.

## Despliegue

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform fmt -check
terraform validate
terraform plan -out=final.tfplan
terraform apply final.tfplan
terraform output
```

Validacion:

```bash
curl "$(terraform output -raw health_url)"
curl "$(terraform output -raw api_test_url)"
```

Prueba de carga:

```bash
python3 ../load-tests/load_test.py \
  "$(terraform output -raw application_url)/work?iterations=100000" \
  --requests 300 --concurrency 30
```

## Limpieza

La destruccion solo debe ejecutarse despues de grabar todas las evidencias.

```bash
terraform destroy
```

La contrasena de RDS es generada por Terraform y no se publica en outputs, archivos
ni en el repositorio. El puerto 5432 solo acepta conexiones desde el Security Group
de la aplicacion.
