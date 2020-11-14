import os
import sys
import boto3

# AWS configurations

session = boto3.Session()

credentials = session.get_credentials()
S3_KEY = credentials.access_key
S3_SECRET = credentials.secret_key
S3_BUCKET = "flask-s3-crop"