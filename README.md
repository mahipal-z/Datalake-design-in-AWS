# Data lake implementation with AWS
Implementation of data lake design using CloudFormation and farm-yield analytics.

![](/lake.PNG)


## Summary
This project has three major deliverables.
1. CloudFormation stack with given AWS resources that works as a ETL pipeline.
2. Analysis of farm yield dataset with 1000 records to find useful insights.
3. Development of ML Application that can predict farm-yield based on user input.

## Part-I CloudFormation
Using the CloudFormation template I developed, one can create a stack to build an ETL pipeline that works as following:
* Upon pipeline activation, a Lambda function will copy the files in the source as is and upload them to the Raw bucket of the Storage Layer.
* Upon upload completion, a python shell Glue job will automatically start. This job will combine both files and upload the combined file to the Processed S3 bucket.
* Upon upload completion, an Apache spark Glue job will be automatically kicked off. This job will create a new column, namely yield_per_hectare. This column is the result of dividing the yield column by the area. This job will also convert the file to parquet format and store the resulting file in the Transformed S3 bucket.

### Prerequisites
A. An S3 bucket that acts as a source, where CSV files are uploaded daily. Following three files must be stored in the bucket's root directory.
> 1. 'run_configurations.config', 2. 'combine_csv.py', 3. 'csvtoparquet.py'

B. The CSV files must be uploaded in the folder named as the current date in 'YYYY-MM-DD' format. 
C. All the CSV files have the same schema.

### Setup instructions
1. Create a CloudFormation stack using the 'cf_template.yml'. Input source bucket name and local timezone when prompted. Refer to https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568 for list of acceptable string for timezone names. 
2. To activate the pipeline, first create a folder named as the current date in 'YYYY-MM-DD' format and upload the 'run_configurations.config' along with all the CSV files to be processed inside the folder, in the source bucket.
