# job_search/aws_secrets.py
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import os
import sys

class ParameterStoreError(Exception):
    """Raised when Parameter Store is unavailable"""
    pass

def get_parameter(parameter_name, required=True):
    try:
        ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=True
        )
        value = response['Parameter']['Value']
        return value
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ParameterNotFound':
            error_msg = f"Parameter '{parameter_name}' not found in Parameter Store"
        else:
            error_msg = f"AWS Error accessing '{parameter_name}': {error_code}"
        
        if required:
            print(f"✗ ERROR: {error_msg}", file=sys.stderr)
            raise ParameterStoreError(error_msg)
        else:
            print(f"⚠ Warning: {error_msg}")
            return None
            
    except NoCredentialsError:
        error_msg = "AWS credentials not configured. Run 'aws configure' or set IAM role."
        print(f"✗ ERROR: {error_msg}", file=sys.stderr)
        if required:
            raise ParameterStoreError(error_msg)
        return None
        
    except Exception as e:
        error_msg = f"Unexpected error fetching '{parameter_name}': {str(e)}"
        print(f"✗ ERROR: {error_msg}", file=sys.stderr)
        if required:
            raise ParameterStoreError(error_msg)
        return None


def get_all_app_parameters(path='/job-search/', required_params=None):
    if required_params is None:
        required_params = []
    
    try:
        ssm = boto3.client('ssm', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        
        parameters = {}
        paginator = ssm.get_paginator('get_parameters_by_path')
        
        for page in paginator.paginate(
            Path=path,
            Recursive=True,
            WithDecryption=True
        ):
            for param in page['Parameters']:
                key = param['Name'].replace(path, '').lstrip('/')
                parameters[key] = param['Value']
                
        
        # Validate required parameters
        missing = [p for p in required_params if p not in parameters]
        if missing:
            error_msg = f"Required parameters missing: {', '.join(missing)}"
            print(f"✗ ERROR: {error_msg}", file=sys.stderr)
            raise ParameterStoreError(error_msg)
        
        return parameters
        
    except NoCredentialsError:
        error_msg = "AWS credentials not configured"
        print(f"✗ ERROR: {error_msg}", file=sys.stderr)
        raise ParameterStoreError(error_msg)
        
    except Exception as e:
        if 'ParameterStoreError' in str(type(e)):
            raise
        error_msg = f"Error loading parameters from {path}: {str(e)}"
        print(f"✗ ERROR: {error_msg}", file=sys.stderr)
        raise ParameterStoreError(error_msg)