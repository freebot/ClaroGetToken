import requests
import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class T1ComerciosAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth_url = 'https://loginclaro.com/auth/realms/plataforma-claro/protocol/openid-connect/token'
        
    def get_token(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        data = {
            'client_id': 'integradores',
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }
        
        try:
            logger.info("Making request to auth endpoint")
            logger.info(f"Request headers: {headers}")
            logger.info(f"Request data: {data}")
            
            response = requests.post(self.auth_url, headers=headers, data=data)
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting token: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Error details: {e.response.text}")
            return None

def store_tokens_in_parameter_store(token_response):
    ssm = boto3.client('ssm')
    
    # Store access token
    ssm.put_parameter(
        Name='/claroshop/access-token',
        Value=token_response['access_token'],
        Type='SecureString',
        Overwrite=True
    )
    
    # Store refresh token
    if 'refresh_token' in token_response:
        ssm.put_parameter(
            Name='/claroshop/refresh-token',
            Value=token_response['refresh_token'],
            Type='SecureString',
            Overwrite=True
        )

def lambda_handler(event, context):
    try:
        # Get credentials from environment variables
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        
        logger.info(f"Checking credentials - Username exists: {bool(username)}, Password exists: {bool(password)}")
        
        if not username or not password:
            error_msg = "Missing environment variables USERNAME or PASSWORD"
            logger.error(error_msg)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': error_msg})
            }
        
        auth = T1ComerciosAuth(username, password)
        token_response = auth.get_token()
        
        if token_response:
            logger.info("Successfully obtained tokens")
            store_tokens_in_parameter_store(token_response)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Tokens successfully obtained and stored',
                    'expires_in': token_response.get('expires_in'),
                    'token_type': token_response.get('token_type'),
                    'scope': token_response.get('scope')
                })
            }
        else:
            error_msg = "Failed to obtain tokens"
            logger.error(error_msg)
            return {
                'statusCode': 500,
                'body': json.dumps({'error': error_msg})
            }
            
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_msg})
        }