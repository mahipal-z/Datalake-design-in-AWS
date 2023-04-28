# This script is used by a glueetl job to transform the merged CSV file. 
# This code adds a column in the dataset and converts the daatframe into Parquet format.

import sys
import boto3
import pandas as pd
#import time
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
sqlContext = SQLContext(sc)
# Define the S3 bucket names and file paths
args = getResolvedOptions(sys.argv, ['transformed_bucket_name', 'processed_bucket_name', 's3_dir'])
print("args:{}".format(args))
src_bucket = args['processed_bucket_name']
dest_bucket = args['transformed_bucket_name']
prefix = args['s3_dir']
print("src_bucket:{}".format(src_bucket))

src_file = 'combined_file.csv'
dest_file = 'transformed_file.parquet'

dest_prefix = prefix

# Initialize the S3 client
s3 = boto3.client('s3')

# Read the CSV files from S3 into pandas dataframes
df = pd.read_csv(f's3://{src_bucket}/{prefix}{src_file}')

# Adding a new column
df['yield_per_hectare'] = df['yield'] / df['area']
df['yield_per_hectare'] = df['yield_per_hectare'].round(3)

# Check if folder with same name exists in destination bucket and delete it
existing_objects = s3.list_objects_v2(Bucket=dest_bucket, Prefix=dest_prefix)
if 'Contents' in existing_objects:
  delete_keys = [{'Key': obj['Key']} for obj in existing_objects['Contents']]
  s3.delete_objects(Bucket=dest_bucket, Delete={'Objects': delete_keys})

# Convert Pandas dataframe to Spark SQL Dataframe
spark_df = sqlContext.createDataFrame(df)

# Convert the DataFrame to a DynamicFrame
dynamic_frame = DynamicFrame.fromDF(spark_df, glueContext, 'combined_file')

# Define the output S3 prefix for the Parquet file
output_prefix = f's3://{dest_bucket}/{dest_prefix}'

#time.sleep(10)

#AWS Glue is based on Apache Spark, which partitions data across multiple nodes to achieve high throughput. 
# When writing data to a file-based sink like Amazon S3, Glue will write a separate file for each partition automatically.
#To merge those files back to single file, we need to use .coalesce() method.
merged_frame = dynamic_frame.coalesce(1)
# Write the DynamicFrame to the output S3 path in Parquet format
glueContext.write_dynamic_frame.from_options(
    frame = merged_frame,
    connection_type = "s3",
    connection_options = {"path": output_prefix},
    format = "parquet"
)
