import boto3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import datetime
from awsglue.utils import getResolvedOptions
import sys

# Define the S3 bucket names and file paths
args = getResolvedOptions(sys.argv, ['transformed_bucket_name', 'processed_bucket_name'])
print("args:{}".format(args))
src_bucket = args['processed_bucket_name']
dest_bucket = args['transformed_bucket_name']
print("src_bucket:{}".format(src_bucket))

src_file = 'combined_file.csv'
dest_file = 'transformed_file.parquet'

today = datetime.datetime.today().strftime('%Y-%m-%d')
src_prefix = today + '/'
dest_prefix = today + '/'

# Initialize the S3 client
s3 = boto3.client('s3')

# Read the CSV files from S3 into pandas dataframes
df = pd.read_csv(f's3://{src_bucket}/{today}/{src_file}')

# Adding a new column
df['yield_per_hectare'] = df['yield'] / df['area']

# Check if folder with same name exists in destination bucket and delete it
existing_objects = s3.list_objects_v2(Bucket=dest_bucket, Prefix=dest_prefix)
if 'Contents' in existing_objects:
  delete_keys = [{'Key': obj['Key']} for obj in existing_objects['Contents']]
  s3.delete_objects(Bucket=dest_bucket, Delete={'Objects': delete_keys})

# Writing the transformed dataframe to a Parquet file in a destination S3 bucket
table = pa.Table.from_pandas(df)
pq.write_table(table, f"s3://{dest_bucket}/{today}/{dest_file}")

