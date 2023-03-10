import boto3
import pandas as pd

# Define the S3 bucket names and file paths
src_bucket = 'datalake-raw-s3-mz'
dest_bucket = 'datalake-processed-s3-mz'
src_file1 = 'dataset - 1.csv'
src_file2 = 'dataset - 2.csv'
dest_file = 'combined_file.csv'

# Initialize the S3 client
s3 = boto3.client('s3')

# Read the CSV files from S3 into pandas dataframes
df1 = pd.read_csv(f's3://{src_bucket}/{src_file1}')
df2 = pd.read_csv(f's3://{src_bucket}/{src_file2}')

# Combine the dataframes into one
combined_df = pd.concat([df1, df2], ignore_index=True)

# Write the combined dataframe to S3 as a CSV file
combined_df.to_csv(dest_file)

# Upload the resulting file to the destination S3 bucket
s3.upload_file(dest_file, dest_bucket, dest_file)
