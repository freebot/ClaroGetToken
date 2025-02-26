
README.md
Apply
# Función Lambda para Tokens de Amazon Selling Partner APIEsta función Lambda automatiza la obtención y almacenamiento de tokens de autenticación para la API de Amazon Selling Partner.## DescripciónLa función realiza las siguientes operaciones:1. Obtiene credenciales (Client ID y Client Secret) desde variables de entorno2. Solicita tokens de autenticación a Amazon3. Almacena los tokens en AWS Parameter Store de forma segura## Requisitos Previos- Cuenta AWS con acceso a:  - AWS Lambda  - AWS Parameter Store- Credenciales de Amazon Selling Partner API:  - Client ID  - Client Secret## Configuración### Variables de EntornoLa función requiere las siguientes variables de entorno:- `CLIENT_ID`: ID de cliente de la aplicación SP-API- `CLIENT_SECRET`: Secreto del cliente de la aplicación SP-API### Permisos IAMLa función necesita los siguientes permisos IAM:```json{    "Version": "2012-10-17",    "Statement": [        {            "Effect": "Allow",            "Action": [                "ssm:PutParameter"            ],            "Resource": [                "arn:aws:ssm:*:*:parameter/                sp-api/*"            ]        }    ]}
Despliegue
Instalar dependencias:
bash
Run
pip install requests boto3 -t .
Crear el archivo ZIP para despliegue:
bash
Run
zip -r function.zip .
Subir el archivo ZIP a AWS Lambda
Uso
La función se puede invocar manualmente o programar con un EventBridge (CloudWatch Events).

Parámetros Almacenados
Los tokens se almacenan en Parameter Store en las siguientes rutas:

Access Token: /sp-api/access-token
Refresh Token: /sp-api/refresh-token
Respuesta de la Función
Éxito
json

{    "statusCode": 200,    "body": {"message": "Tokens successfully     updated"}}
Error
json

{    "statusCode": 500,    "body": {"error": "Error message"}}
Mantenimiento
Se recomienda configurar alertas de CloudWatch para monitorear:

Errores de ejecución
Tiempos de ejecución
Fallos en la obtención de tokens


