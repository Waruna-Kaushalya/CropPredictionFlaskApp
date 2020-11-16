import os
import sys
import boto3

# AWS configurations

S3_BUCKET = "flask-s3-crop"
# S3_KEY                    = "AKIA4YEQCWGSDZANPYOB"
# S3_SECRET                 = "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"

# session = boto3.Session()
# credentials = session.get_credentials()
# S3_KEY = credentials.access_key
# S3_SECRET = credentials.secret_key

from boto.s3.connection import S3Connection
# s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])

S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']

