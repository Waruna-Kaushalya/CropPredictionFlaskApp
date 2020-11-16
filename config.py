import os
import sys
import boto3

# AWS configurations

# S3_BUCKET = "flask-s3-crop"

try:
    # Local server
    session = boto3.Session()
    credentials = session.get_credentials()
    S3_KEY = credentials.access_key
    S3_SECRET = credentials.secret_key

except:
    # Heroku
    from boto.s3.connection import S3Connection
    S3_KEY = os.environ['S3_KEY']
    S3_SECRET = os.environ['S3_SECRET']
    S3_BUCKET = os.environ['S3_BUCKET']

    

