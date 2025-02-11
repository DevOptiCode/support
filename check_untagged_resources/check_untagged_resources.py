#!/usr/bin/env python3

import boto3
import argparse
import pandas as pd

def get_untagged_resources(aws_access_key, aws_secret_key, region, resources=None):
    # Initialize a session, use IAM role if no access/secret key is provided
    if aws_access_key and aws_secret_key:
        session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region
        )
    else:
        session = boto3.Session(region_name=region)  # Use default profile

    # Initialize clients for EC2, S3, RDS, and Lambda
    ec2 = session.client('ec2')
    s3 = session.client('s3')
    rds = session.client('rds')
    lambda_client = session.client('lambda')

    # Define the resource types to check
    resource_types = resources if resources else ['ec2', 's3', 'rds', 'lambda']

    # Placeholder for untagged resources
    untagged_resources = []

    # Check EC2 instances and EBS volumes
    if 'ec2' in resource_types:
        # Fetch all EC2 instances
        instances = ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                tags = instance.get('Tags', [])
                if not tags:
                    untagged_resources.append({
                        'Resource Type': 'EC2 Instance',
                        'Resource ID': instance['InstanceId'],
                        'Resource Name': 'N/A'
                    })
                else:
                    # Extract resource name if available
                    name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                    untagged_resources.append({
                        'Resource Type': 'EC2 Instance',
                        'Resource ID': instance['InstanceId'],
                        'Resource Name': name_tag
                    })
        
        # Fetch all EBS volumes
        volumes = ec2.describe_volumes()
        for volume in volumes['Volumes']:
            tags = volume.get('Tags', [])
            if not tags:
                untagged_resources.append({
                    'Resource Type': 'EBS Volume',
                    'Resource ID': volume['VolumeId'],
                    'Resource Name': 'N/A'
                })
            else:
                # Extract resource name if available
                name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                untagged_resources.append({
                    'Resource Type': 'EBS Volume',
                    'Resource ID': volume['VolumeId'],
                    'Resource Name': name_tag
                })

    # Check S3 buckets
    if 's3' in resource_types:
        # Fetch all S3 buckets
        buckets = s3.list_buckets()
        for bucket in buckets['Buckets']:
            # Fetch tags for each bucket
            try:
                tags = s3.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
                if not tags:
                    untagged_resources.append({
                        'Resource Type': 'S3 Bucket',
                        'Resource ID': bucket['Name'],
                        'Resource Name': 'N/A'
                    })
                else:
                    # Extract resource name if available
                    name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                    untagged_resources.append({
                        'Resource Type': 'S3 Bucket',
                        'Resource ID': bucket['Name'],
                        'Resource Name': name_tag
                    })
            except s3.exceptions.ClientError:
                # Skip buckets that cannot be tagged
                continue

    # Check RDS instances
    if 'rds' in resource_types:
        # Fetch all RDS instances
        db_instances = rds.describe_db_instances()
        for db_instance in db_instances['DBInstances']:
            tags = rds.list_tags_for_resource(ResourceName=db_instance['DBInstanceArn']).get('TagList', [])
            if not tags:
                untagged_resources.append({
                    'Resource Type': 'RDS Instance',
                    'Resource ID': db_instance['DBInstanceIdentifier'],
                    'Resource Name': 'N/A'
                })
            else:
                # Extract resource name if available
                name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), 'N/A')
                untagged_resources.append({
                    'Resource Type': 'RDS Instance',
                    'Resource ID': db_instance['DBInstanceIdentifier'],
                    'Resource Name': name_tag
                })

    # Check Lambda functions
    if 'lambda' in resource_types:
        # Fetch all Lambda functions
        functions = lambda_client.list_functions()
        for function in functions['Functions']:
            tags = lambda_client.list_tags(Resource=function['FunctionArn']).get('Tags', {})
            if not tags:
                untagged_resources.append({
                    'Resource Type': 'Lambda Function',
                    'Resource ID': function['FunctionName'],
                    'Resource Name': 'N/A'
                })
            else:
                # Extract resource name if available
                name_tag = tags.get('Name', 'N/A')
                untagged_resources.append({
                    'Resource Type': 'Lambda Function',
                    'Resource ID': function['FunctionName'],
                    'Resource Name': name_tag
                })

    # Convert untagged resources to a DataFrame for easier display
    df = pd.DataFrame(untagged_resources)

    return df


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Check for untagged AWS resources')
    parser.add_argument('--aws-access-key', required=False, help='AWS Access Key')
    parser.add_argument('--aws-secret-key', required=False, help='AWS Secret Key')
    parser.add_argument('--region', required=True, help='AWS Region')
    parser.add_argument('--resources', nargs='*', help='Comma-separated list of resource types to check (optional)')
    
    args = parser.parse_args()

    # Get untagged resources
    untagged_df = get_untagged_resources(
        args.aws_access_key, args.aws_secret_key, args.region, args.resources
    )

    if not untagged_df.empty:
        print(untagged_df)
    else:
        print("No untagged resources found.")

