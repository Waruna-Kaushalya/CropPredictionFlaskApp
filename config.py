import os
import sys
import boto3

# AWS configurations

S3_BUCKET = "flask-s3-crop"
S3_KEY                    = "AKIA4YEQCWGSDZANPYOB"
S3_SECRET                 = "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"

# session = boto3.Session()
# credentials = session.get_credentials()
# S3_KEY = credentials.access_key
# S3_SECRET = credentials.secret_key