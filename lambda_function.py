import json
import base64
import requests
import os
import boto3

def lambda_handler(event, context):
    # Get credentials from environment variables
    client_id = os.environ.get('CLIENT_ID')
    client_secret = os.environ.get('CLIENT_SECRET')
    
    if not client_id or not client_secret:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Missing environment variables'})
        }
    
    token_response = get_lwa_token(client_id, client_secret)
    if token_response:
        # Store tokens in Parameter Store
        store_tokens_in_parameter_store(token_response)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Tokens successfully updated'})
        }
    
    return {
        'statusCode': 500,
        'body': json.dumps({'error': 'Failed to get token'})
    }

def get_lwa_token(client_id, client_secret):
    token_url = 'https://api.amazon.com/auth/o2/token'
    
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Authorization': f'Basic {encoded_credentials}'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'scope': 'role::sellingpartnerapi::app'
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting LWA token: {e}")
        if hasattr(e.response, 'text'):
            print(f"Error details: {e.response.text}")
        return None

def store_tokens_in_parameter_store(token_response):
    ssm = boto3.client('ssm')
    
    # Store access token
    ssm.put_parameter(
        Name='/sp-api/access-token',
        Value=token_response['access_token'],
        Type='SecureString',
        Overwrite=True
    )
    
    # Store refresh token if present
    if 'refresh_token' in token_response:
        ssm.put_parameter(
            Name='/sp-api/refresh-token',
            Value=token_response['refresh_token'],
            Type='SecureString',
            Overwrite=True
        )