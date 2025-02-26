
# Función Lambda para Tokens de Claroshop API

Esta función Lambda automatiza la obtención y almacenamiento de tokens de autenticación para la API de Claroshop.

## Descripción

La función realiza las siguientes operaciones:
1. Obtiene credenciales (Client ID y Client Secret) desde variables de entorno
2. Solicita tokens de autenticación a Claroshop
3. Almacena los tokens en AWS Parameter Store de forma segura

## Requisitos Previos

- Cuenta AWS con acceso a:
  - AWS Lambda
  - AWS Parameter Store
- Credenciales de Claroshop API:
  - Client ID
  - Client Secret

## Configuración

### Variables de Entorno

La función requiere las siguientes variables de entorno:

- `CLIENT_ID`: ID de cliente de la aplicación Claroshop
- `CLIENT_SECRET`: Secreto del cliente de la aplicación Claroshop

### Permisos IAM

La función necesita los siguientes permisos IAM:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:PutParameter"
            ],
            "Resource": [
                "arn:aws:ssm:*:*:parameter/claroshop/*"
            ]
        }
    ]
}
```

## Despliegue

1. Instalar dependencias:
```bash
pip install requests boto3 -t .
```

2. Crear el archivo ZIP para despliegue:
```bash
zip -r function.zip .
```

3. Subir el archivo ZIP a AWS Lambda

## Uso

La función se puede invocar manualmente o programar con un EventBridge (CloudWatch Events).

### Parámetros Almacenados

Los tokens se almacenan en Parameter Store en las siguientes rutas:
- Access Token: `/claroshop/access-token`
- Refresh Token: `/claroshop/refresh-token`

## Respuesta de la Función

### Éxito
```json
{
    "statusCode": 200,
    "body": {"message": "Tokens successfully updated"}
}
```

### Error
```json
{
    "statusCode": 500,
    "body": {"error": "Error message"}
}
```

## Mantenimiento

Se recomienda configurar alertas de CloudWatch para monitorear:
- Errores de ejecución
- Tiempos de ejecución
- Fallos en la obtención de tokens
```

Los principales cambios realizados fueron:
1. Cambio de nombre y referencias de Amazon Selling Partner API a Claroshop API
2. Actualización de las rutas de Parameter Store de `/sp-api/` a `/claroshop/`
3. Actualización de las referencias a las credenciales para reflejar Claroshop en lugar de SP-API
4. Mantenimiento de la estructura general del documento pero con el contexto correcto