# AWS Untagged Resources Checker

This Python script helps identify untagged AWS resources in your account. It can check EC2 instances, EBS volumes, S3 buckets, RDS instances, and Lambda functions. You can provide specific resources to check or let the script check all resources by default. The script can use IAM profiles or explicit AWS access keys and secret keys for authentication.

## Features

- Check for untagged resources in the following services:
  - **EC2 Instances** (including EBS volumes)
  - **S3 Buckets**
  - **RDS Instances**
  - **Lambda Functions**
  
- Use default IAM profile credentials if no AWS access key or secret is provided.
- Accept a list of specific resources to check or check all by default.
- Display the untagged resources in a readable format (either printed in the console or displayed using an optional tool).

## Requirements

- Python 3.6 or later
- `boto3` package (for AWS API interaction)
- `pandas` package (for organizing the results)
- Optional: `ace-tools` for displaying the results in a UI (can be removed or replaced with direct print statements)

## Installation

1. Clone or download the repository.
2. Install the required dependencies by running:

   ```bash
   pip install boto3 pandas
   ```

## Configuration
You can either use an AWS IAM profile or explicitly provide your AWS credentials (Access Key ID and Secret Key) for authentication. The script automatically uses the default IAM profile if no credentials are provided.


## Usage
1. Using IAM Profile (No Credentials Needed)
If your environment is configured with an AWS IAM profile that has appropriate permissions, you can run the script without specifying AWS credentials.

### Example command:
```bash
python check_untagged_resources.py --region YOUR_REGION --resources ec2 s3 rds lambda
```

##### Where:
--region is the AWS region (e.g., us-east-1, eu-west-1).
--resources is an optional list of resource types to check (e.g., ec2, s3, rds, lambda). If no resources are specified, the script checks all resources.

2. Using AWS Access Key and Secret Key
If you want to use explicit AWS credentials, provide them using the --aws-access-key and --aws-secret-key arguments.

##### Example command:
```bash
python check_untagged_resources.py --aws-access-key YOUR_ACCESS_KEY --aws-secret-key YOUR_SECRET_KEY --region YOUR_REGION --resources ec2 s3 rds lambda
```

##### Where:
--aws-access-key and --aws-secret-key are your AWS credentials.
--region is the AWS region.
--resources is an optional list of resource types to check (e.g., ec2, s3, rds, lambda). If not provided, the script checks all resources.

3. Output
The script will print the untagged resources in your terminal or command line as a tabular format. If ace-tools is installed, it will display the results in a more user-friendly table format.

##### Example Output
If untagged resources are found, the script will display a table with columns for resource type, ID, and name.

Example:

```bash
Resource Type   | Resource ID          | Resource Name
--------------------------------------------------------
EC2 Instance    | i-1234567890abcdef0  | N/A
S3 Bucket       | my-bucket-name       | N/A
Lambda Function | my-lambda-function   | N/A
```

If no untagged resources are found, the script will print:
```bash
No untagged resources found.
```