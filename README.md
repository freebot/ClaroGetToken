
# ClaroShop Token Lambda Function

Lambda function that obtains and stores authentication tokens for ClaroShop's API integration.

## Description

This function automates the process of:
1. Authenticating with ClaroShop's API
2. Obtaining access and refresh tokens
3. Storing tokens securely in AWS Parameter Store

## Requirements

- AWS Account with access to:
  - AWS Lambda
  - AWS Systems Manager Parameter Store
- ClaroShop API Credentials:
  - Username
  - Password

## Configuration

### Environment Variables

The function requires these environment variables:
- `CLAROSHOP_USERNAME`: Your ClaroShop API username
- `CLAROSHOP_PASSWORD`: Your ClaroShop API password

### IAM Permissions

The Lambda function's role needs these permissions:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:PutParameter",
                "ssm:GetParameter",
                "ssm:DeleteParameter"
            ],
            "Resource": "arn:aws:ssm:us-east-1:800444307139:parameter/claroshop/*"
        }
    ]
}

## Deployment
1. Install dependencies:
```bash
pip install requests boto3 -t .
 ```

2. Create deployment package:
```bash
zip -r function.zip .
 ```

3. Upload to AWS Lambda
## Stored Parameters
The function stores these parameters in AWS Parameter Store:

- /claroshop/access_token
- /claroshop/refresh_token
- /claroshop/expires_in
- /claroshop/refresh_expires_in
- /claroshop/token_type
- /claroshop/scope
- /claroshop/session_state
- /claroshop/not-before-policy
## Response Format
### Success
```json
{
    "statusCode": 200,
    "body": {
        "message": "ClaroShop tokens successfully obtained and stored",
        "expires_in": 300,
        "token_type": "Bearer",
        "scope": "..."
    }
}
 ```
```

### Error
```json
{
    "statusCode": 500,
    "body": {
        "error": "Error message"
    }
}
 ```

## Monitoring
Monitor the function using CloudWatch Logs for:

- Authentication failures
- Token storage issues
- General execution errors