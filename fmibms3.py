import os
import sys
from ibm_botocore.client import Config
import ibm_boto3

api_key = os.environ['cos_api_key']
service_instance_id = os.environ['cos_resource_instance_id']
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.us-east.objectstorage.softlayer.net'
cos = ibm_boto3.resource('s3',
                      ibm_api_key_id=api_key,
                      ibm_service_instance_id=service_instance_id,
                      ibm_auth_endpoint=auth_endpoint,
                      config=Config(signature_version='oauth'),
                      endpoint_url=service_endpoint)

def create_item(bucket_name, item_name, file_text):
    print("Create new item: {0}".format(item_name))
    try:
        cos.Object(bucket_name, item_name).put(
            Body=file_text
        )
        print("Item {0} created!".format(item_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create text file: {0}".format(e))

def get_item(bucket_name, item_name):
    print("Retrieving item from bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        file = cos.Object(bucket_name, item_name).get()
        data = file["Body"].read()
        print("File Contents: {0}".format(data))
        return data
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to retrieve file contents: {0}".format(e))

def put_item(bucket_name, item_name, path):
        print("Putting item to bucket: {0}, key: {1}".format(bucket_name, item_name))
        try:
            file = open(item_name,'rb')
            cos.Bucket(bucket_name).put_object(Key=item_name,Body=file)
            print("File contents: {0} added".format(item_name))
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to put file contents: {0}".format(e))

def download_item(bucket_name, item_name, path):
    print("Downloading item from the bucket: {0}, key: {1}".format(bucket_name, item_name))
    try:
        cos.meta.client.download_file(bucket_name, item_name, path)
        print("File contents: {0} added to {1}".format(item_name,path))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to download file contents: {0}".format(e))
