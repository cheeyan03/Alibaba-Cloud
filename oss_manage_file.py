import oss2
import os
from dotenv import load_dotenv
from oss2.credentials import EnvironmentVariableCredentialsProvider

load_dotenv()

auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
endpoint = "https://oss-ap-southeast-3.aliyuncs.com"
region = "ap-southeast-3"
bucket_name = "ai-hackathon-transaction1"
bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)

def upload_to_oss(filename, file_content):
    bucket.put_object(filename, file_content)
    return f"https://{bucket_name}.oss-ap-southeast-3.aliyuncs.com/{filename}"

# # -*- coding: utf-8 -*-
# import oss2
# from oss2.credentials import EnvironmentVariableCredentialsProvider
# from itertools import islice
# import os
# import logging
# import time
# import random
# from dotenv import load_dotenv

# load_dotenv()  # Load from .env

# # oss_access_key_id = os.environ('OSS_ACCESS_KEY_ID')
# # oss_access_key_secret = os.environ('OSS_ACCESS_KEY_SECRET')
# # Configure logs.
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# # Check whether the environment variables are configured.
# required_env_vars = ['OSS_ACCESS_KEY_ID', 'OSS_ACCESS_KEY_SECRET']
# for var in required_env_vars:
#     if var not in os.environ:
#         logging.error(f"Environment variable {var} is not set.")
#         exit(1)

# def generate_unique_bucket_name():
#     # Query the current timestamp.
#     timestamp = int(time.time())
#     # Generate a random number from 0 to 9999.
#     random_number = random.randint(0, 9999)
#     # Specify the name of the bucket. The name must be globally unique.
#     bucket_name = f"demo-{timestamp}-{random_number}"
#     return bucket_name

# def create_bucket(bucket):
#     try:
#         bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
#         logging.info("Bucket created successfully")
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to create bucket: {e}")

# def upload_file(bucket, object_name, data):
#     try:
#         result = bucket.put_object(object_name, data)
#         logging.info(f"File uploaded successfully, status code: {result.status}")
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to upload file: {e}")

# def download_file(bucket, object_name):
#     try:
#         file_obj = bucket.get_object(object_name)
#         content = file_obj.read().decode('utf-8')
#         logging.info("File content:")
#         logging.info(content)
#         return content
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to download file: {e}")

# def list_objects(bucket):
#     try:
#         objects = list(islice(oss2.ObjectIterator(bucket), 10))
#         for obj in objects:
#             logging.info(obj.key)
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to list objects: {e}")

# def delete_objects(bucket):
#     try:
#         objects = list(islice(oss2.ObjectIterator(bucket), 100))
#         if objects:
#             for obj in objects:
#                 bucket.delete_object(obj.key)
#                 logging.info(f"Deleted object: {obj.key}")
#         else:
#             logging.info("No objects to delete")
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to delete objects: {e}")

# def delete_bucket(bucket):
#     try:
#         bucket.delete_bucket()
#         logging.info("Bucket deleted successfully")
#     except oss2.exceptions.OssError as e:
#         logging.error(f"Failed to delete bucket: {e}")

# # The following sample code provides an example of the main process of using OSS SDK for Python to perform common operations.
# if __name__ == '__main__':
#     # # 1: Create a bucket.
#     # Generate a unique bucket name.
#     # bucket_name = generate_unique_bucket_name()
#     # bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)
#     # create_bucket(bucket)

#     # Obtain access credentials from environment variables.
#     auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())

#     # Specify the endpoint and region.
#     endpoint = "https://oss-ap-southeast-3.aliyuncs.com"
#     region = "ap-southeast-3"

#     # Create a bucket instance.
#     bucket_name = "ai-hackathon-transaction1"
#     bucket = oss2.Bucket(auth, endpoint, bucket_name, region=region)
#     # create_bucket(bucket)
#     # 2. Upload a local file to the bucket.
#     upload_file(bucket, 'test-string-file', b'Hello OSS, this is a test string.')
#     # 3. Download an object from the bucket.
#     download_file(bucket, 'test-string-file')
#     # 4. List objects in the bucket.
#     # list_objects(bucket)
#     # 5. Delete an object from the bucket.
#     # delete_objects(bucket)
#     # 6. Delete a bucket.
#     # delete_bucket(bucket)
    