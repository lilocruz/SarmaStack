# SarmaStack is an Infrastructure as Code (IaC) tool designed to simplify the provisioning and management of AWS cloud infrastructure resources. 
# With SarmaStack, you can define your AWS infrastructure configurations in a declarative manner and easily create and manage your resources.

# Author: Michael Cruz Sanchez (Search Engineer @lucidworks)
# Copyright: GPLv3

import argparse
import boto3
import yaml

def create_instance(args):
    if args.get('file'):
        with open(args['file'], 'r') as f:
            data = yaml.save_load(f)
            instances = data.get('instances')
            if instances:
                for instance in instances:
                    create_instance(instance)
            else:
                print("No instances specifications found in the YAML file.")

    else:
        ec2_client = boto3.client('ec2')
        instance_name = args.get('instance_name') or 'name'
        response = ec2_client.run_instances(
            ImageId=args['image_id'],
            InstanceType=args['instance_type'],
            MinCount=1,
            MaxCount=1,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_name
                        },
                    ]
                },
            ]
        )
        print(f"Created instance with id {args['image_id']} and name: {args[instance_name]}")

def stop_instance(args):
    ec2_client = boto3.client('ec2')
    response = ec2_client.stop_instances(
        InstanceIds=[args['instance_id']]
    )
    print(f"Stopped EC2 instance with ID: {args['instance_id']}")

def delete_instance(args):
    if args.get('file'):
        with open(args['file'], 'r') as f:
            data = yaml.save_load(f)
            instances = data.get('instances')
            if instances:
                instance_ids = [instance['instance_id'] for instance in instances]
                delete_instance({'instance_ids': instance_ids})
            else:
                print("No instance specifications found in the YAML file.")
    
    else:
        # Delete the instances using the CLI arguments
        ec2_client = boto3.client('ec2')
        instance_ids = args.get('instance_ids')
        if instance_ids:
            response = ec2_client.terminate_instances(InstanceIds=instance_ids)
            print(f"Deleted instances: {args['instance_ids']}")

def create_bucket(args):
    s3_client = boto3.client('s3')
    response = s3_client.create_bucket(
        Bucket=args['name'],
        CreateBucketConfiguration={
            'LocationConstraint': args['region']
        }
    )
    print(f"Created bucket: args{['bucket_name']}")

def delete_bucket(args):
    s3_client = boto3.client('s3')
    s3_client.delete_bucket(Bucket=args['name'])
    print(f"Deleted S3 bucket: {args['name']}")

def create_iam_user(args):
    iam_client = boto3.client('iam')
    response = iam_client.create_user(
        UserName=args['name']
    )
    print(f"Created IAM user: {args['name']}")

def create_iam_role(args):
    iam_client = boto3.client('iam')
    response = iam_client.create_role(
        RoleName=args['role_name'],
        AssumeRolePolicyDocument=args['assume_role_policy']
    )
    print(f"Created IAM role: {args['role_name']}")

def create_iam_policy(args):
    iam_client = boto3.client('iam')
    with open(args['policy_document'], 'r') as f:
        policy_document = f.read()
    response = iam_client.create_policy(
        PolicyName=args['policy_name'],
        PolicyDocument=policy_document
    )
    print(f"Created IAM policy: {args['policy_name']}")

def suggest_ami(args):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_images(
        Filters=[
            {
                'Name': args['filter_name'],
                'Values': args['filter_values']
            }
        ]
    )
    ami_ids = [image['ImageId'] for image in response['Images']]
    ami_names = [image['Name'] for image in response['Images']]

    print("Suggested AMI image IDs:")
    for ami_id, ami_name in zip(ami_ids, ami_names):
        print(f"AMI ID: {ami_id}, OS Name: {ami_name}")

def provision(args):
    with open(args['file'], 'r') as f:
        data = yaml.safe_load(f)

    if 'instances' in data:
        instances = data['instances']
        for instance in instances:
            create_instance(instance)
    else:
        print("No instance specifications found in the YAML file.")
    
    if 'buckets' in data:
        buckets = data['buckets']
        for bucket in buckets:
            create_bucket(bucket)
    else:
        print("No bucket specifications found in the YAML file.")

def main():
    # Create the main argument parser
    parser = argparse.ArgumentParser(description='SarmaStack IaC by Michael Cruz Sanchez')

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    # Create a parser for the "create-iam-user" command
    create_iam_user_parser = subparsers.add_parser('create-iam-user', help='Create an IAM user')
    create_iam_user_parser.add_argument('-un', '--user_name', help='Name of the IAM user')

    # Create a parser for the "create-iam-role" command
    create_iam_role_parser = subparsers.add_parser('create-iam-role', help='Create an IAM role')
    create_iam_role_parser.add_argument('-rn', '--role_name', help='Name of the IAM role')
    create_iam_role_parser.add_argument('-asrp', '--assume-role-policy', help='Assume role policy document')

    # Create a parser for the "create-iam-policy" command
    create_iam_policy_parser = subparsers.add_parser('create-iam-poliy', help='Create an IAM policy')
    create_iam_policy_parser.add_argument('-pn', '--policy_name', help='Name of the IAM policy')
    create_iam_policy_parser.add_argument('-pd', '--policy_document', help='Path to the policy document')

    # Create a parser for the "create-instance" command
    create_instance_parser = subparsers.add_parser('create-instance', help='Create an instance')
    create_instance_parser.add_argument('-in', '--instance-name', required=True, help='Name of the instance')
    create_instance_parser.add_argument('-it', '--instance-type', required=True, help='Type of the instance')
    create_instance_parser.add_argument('-id', '--image-id', required=True, help='ID of the AMI image')
    create_instance_parser.add_argument('-f', '--file', help='Path to the YAML file')

    # Create a parser for the "stop-instance" command
    stop_instance_parser = subparsers.add_parser('stop-instance', help='Stop an instance')
    stop_instance_parser.add_argument('-id', '--instance_id', help='ID of the instance')

    # Create a parser for the "delete-instance" command
    delete_instance_parser = subparsers.add_parser('delete-instance', help='Delete an instance')
    delete_instance_parser.add_argument('-id', '--instance_ids', nargs='+', help='ID of the instances to delete')
    delete_instance_parser.add_argument('-f', '--file', help='Path to the YAML file')


    # Create a parser for the "create-bucket" command
    create_bucket_parser = subparsers.add_parser('create-bucket', help='Create a bucket')
    create_bucket_parser.add_argument('-bn', '--bucket_name', help='Name of the bucket')

    # Create a parser for the "delete-bucket" command
    delete_bucket_parser = subparsers.add_parser('delete-bucket', help='Delete a bucket')
    delete_bucket_parser.add_argument('-bn', '--bucket_name', help='Name of the bucket')

    # Create a parser for the "suggest-ami" command
    suggest_ami_parser = subparsers.add_parser('suggest-ami', help='Suggest AMI image IDs')
    suggest_ami_parser.add_argument('-fn', '--filter-name', help='Name of the filter')
    suggest_ami_parser.add_argument('-fv', '--filter-values', nargs='+', help='Values for the filter')

    # Create a parser for the "provision" command
    provision_parser = subparsers.add_parser('provision', help='Provision infrastructure from YAML file')
    provision_parser.add_argument('-f', '--file', help='Path to the YAML file')

    # Parse the command-line arguments
    args = vars(parser.parse_args())

    # Handle the commands
    if args['command'] == 'create-instance':
        create_instance(args)
    elif args['command'] == 'stop-instance':
        stop_instance(args)
    elif args['command'] == 'delete-instance':
        delete_instance(args)
    elif args['command'] == 'create-bucket':
        create_bucket(args)
    elif args['command'] == 'delete-bucket':
        delete_bucket(args)
    elif args['command'] == 'create-iam-user':
        create_iam_user(args)
    elif args['command'] == 'create-iam-role':
        create_iam_role(args)
    elif args['command'] == 'create-iam-policy':
        create_iam_policy(args)
    elif args['command'] == 'suggest-ami':
        suggest_ami(args)
    elif args['command'] == 'provision':
        provision(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

