import boto3
import datetime
import glob
import json
import logging
import os
import random
import uuid
import urllib.parse

from botocore.client import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info('Loading function')

def lambda_handler(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # print (json.dumps(event))
    
    # ID
    assetID = str(uuid.uuid4())
    # Get the object from the event and show its content type
    sourceBucket = event['Records'][0]['s3']['bucket']['name']
    logger.info(sourceBucket)
    sourceKey = event['Records'][0]['s3']['object']['key']
    logger.info(sourceKey)
    sourceS3 = 's3://'+ sourceBucket + '/'
    fullSourceS3 = 's3://'+ sourceBucket + '/' + sourceKey
    logger.info(sourceS3)
    sourceS3Basename = os.path.splitext(os.path.basename(sourceS3))[0]
    logger.info(sourceS3Basename)
    destinationS3 = os.environ['DESTINATION']
    logger.info(destinationS3)
    mediaConvertRole = os.environ['ROLE']
    logger.info(mediaConvertRole)
    region = os.environ['REGION']
    queue = os.environ['QUEUE']
    statusCode = 200
    body = {}
    
    # Use MediaConvert SDK UserMetadata to tag jobs with the assetID 
    # Events from MediaConvert will have the assetID in UserMedata
    jobMetadata = {'assetID': assetID}

    try:
      # Job settings are in the lambda zip file in the current working directory
      with open('job.json') as json_data:
        jobSettings = json.load(json_data)
        print(jobSettings)
      
      # get the account-specific mediaconvert endpoint for this region
      mc = boto3.client('mediaconvert', region_name=region)
      endpoints = mc.describe_endpoints()
            
      # add the account-specific endpoint to the client session 
      client = boto3.client('mediaconvert', region_name=region, endpoint_url=endpoints['Endpoints'][0]['Url'], verify=False)
      
      # Update the job settings with the source video from the S3 event and destination 
      # paths for converted videos
      jobSettings['OutputGroups'][0]['Outputs'][0]['NameModifier'] = assetID
      jobSettings['OutputGroups'][0]['OutputGroupSettings']['FileGroupSettings']['Destination'] = destinationS3 
      jobSettings['Inputs'][0]['FileInput'] = fullSourceS3
      
      #print('Export: ' + str(jobSettings['Inputs'][0]['FileInput']))
      
      #print('jobSettings:')
      #print(json.dumps(jobSettings))
      
      # Convert the video using AWS Elemental MediaConvert
      job = client.create_job(Role=mediaConvertRole, UserMetadata=jobMetadata, Settings=jobSettings)
      print (json.dumps(job, default=str))
      
    except Exception as e:
      print ('Exception: %s' % e)
      statusCode = 500
      raise
    
    finally:
      return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
      }


