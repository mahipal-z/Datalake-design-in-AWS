# This script is used by a python shell glue job to merge multiple csv files.


import boto3
import pandas as pd
import os
from io import StringIO
from awsglue.utils import getResolvedOptions
import sys

# Define the S3 bucket names and file paths
args = getResolvedOptions(sys.argv, ['raw_bucket_name', 'processed_bucket_name', 's3_dir'])
#print("args:{}".format(args))
src_bucket = args['raw_bucket_name']
dest_bucket = args['processed_bucket_name']
prefix = args['s3_dir']
#print("src_bucket:{}".format(src_bucket))

dest_file = 'combined_file.csv'

# Initialize the S3 client
s3 = boto3.client('s3')
 
src_prefix = prefix
dest_prefix = prefix
print("src_prefix:{}".format(src_prefix))

# Get the list of object keys in the input S3 bucket
src_objects = s3.list_objects_v2(Bucket=src_bucket, Prefix=src_prefix)
#print("src_objects:{}".format(src_objects))
object_keys = [obj['Key'] for obj in src_objects['Contents']]
#print("object_keys:{}".format(object_keys))

# Check if folder with same name exists in destination bucket and delete it
existing_objects = s3.list_objects_v2(Bucket=dest_bucket, Prefix=dest_prefix)
if 'Contents' in existing_objects:
  delete_keys = [{'Key': obj['Key']} for obj in existing_objects['Contents']]
  s3.delete_objects(Bucket=dest_bucket, Delete={'Objects': delete_keys})

# Concatenate all CSV files in the input S3 bucket
dfs = []
for key in object_keys:
    if key.endswith('.csv'):
        response = s3.get_object(Bucket=src_bucket, Key=key)
        #print("response:{}".format(response))
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(pd.compat.StringIO(csv_content))
        #print("df:{}".format(df))
        dfs.append(df)
result = pd.concat(dfs, ignore_index=True)

#print("result:{}".format(result))
#In above code, we read the content of the S3 object returned by the get_object API call and decode it from
#  bytes to a string using the utf-8 encoding. The resulting string is the raw CSV data. 
#Then, we create a pandas DataFrame from the CSV data by first wrapping the csv_content string in a StringIO object from
#  the io module using pd.compat.StringIO(csv_content)
#The pd.compat module is used to ensure compatibility between different versions of pandas.
#this approach of reading CSV data from an S3 object into a DataFrame using StringIO is memory efficient and 
# avoids having to store the CSV data in a temporary file on disk. 
# It is suitable for handling large CSV files that may not fit into memory.

# Upload the concatenated CSV file to the output S3 bucket
dest_key = os.path.join(dest_prefix, dest_file)
print("dest_key:{}".format(dest_key))

if not result.empty:
    s3.put_object(Body=result.to_csv(index=False), Bucket=dest_bucket, Key=dest_key)