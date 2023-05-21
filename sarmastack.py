# SarmaStack is an Infrastructure as Code (IaC) tool designed to simplify the provisioning and management of AWS cloud infrastructure resources. 
# With SarmaStack, you can define your AWS infrastructure configurations in a declarative manner and easily create and manage your resources.

# Author: Michael Cruz Sanchez (Search Engineer @lucidworks)
# Copyright: GPLv3

import argparse
import boto3
import yaml
from list import ListManager
from delete import DeleteManager
from create import CreateManager
from stop import StopManager
from network import NetworkManager

manager = ListManager()
delete_manager = DeleteManager()
create_manager = CreateManager()
stop_manager = StopManager()
network_manager = NetworkManager()

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
            create_manager.create_instance(instance)
    else:
        print("No instance specifications found in the YAML file.")
    
    if 'buckets' in data:
        buckets = data['buckets']
        for bucket in buckets:
            create_manager.create_bucket(bucket)
    else:
        print("No bucket specifications found in the YAML file.")
    
    if 'resources' in data:
        resources = data['resources']
        for resource in resources:
            resource_type = resource.get('type')
            if resource_type == 'iam_user':
                create_manager.create_iam_user(resource)
            elif resource_type == 'iam_role':
                create_manager.create_iam_role(resource)
            elif resource_type == 'iam_policy':
                create_manager.create_iam_policy(resource)
            else:
                print(f"Unsupported resource type: {resource_type}")


def main():
    
    #location = aws_manager.get_location_constraint('us-west-2')
    # Create the main argument parser
    parser = argparse.ArgumentParser(description='SarmaStack IaC by Michael Cruz Sanchez')
     # Create subparsers for different commands
    subparsers = parser.add_subparsers(title='Commands', dest='command')

    # Create a parser for the "network" command
    # network_parser = argparse.ArgumentParser(description='Manage AWS Networking')

    # Subparser for the network command
    network_parser = subparsers.add_parser('network', help='Network actions')
    network_parser.add_argument('action', choices=['create-vpc', 'create-subnet', 'create-internet-gateway',
                                              'attach-internet-gateway', 'create-route-table',
                                              'create-route', 'associate-subnet-with-route-table',
                                              'enable-vpc-dns-hostnames'], help='Action to perform')
    network_parser.add_argument('--cidr-block', help='CIDR block for VPC or subnet')
    network_parser.add_argument('--vpc-id', help='ID of the VPC')
    network_parser.add_argument('--availability-zone', help='Availability zone for subnet')
    network_parser.add_argument('--internet-gateway-id', help='ID of the internet gateway')
    network_parser.add_argument('--route-table-id', help='ID of the route table')
    network_parser.add_argument('--destination-cidr-block', help='Destination CIDR block for route')

    # Options for the network command
    # network_parser.add_argument('--cidr-block', help='CIDR block for VPC or subnet')
    # network_parser.add_argument('--availability-zone', help='Availability zone for subnet')
    # network_parser.add_argument('--vpc-id', help='ID of VPC')
    # network_parser.add_argument('--internet-gateway-id', help='ID of internet gateway')
    # network_parser.add_argument('--route-table-id', help='ID of route table')
    # network_parser.add_argument('--destination-cidr-block', help='Destination CIDR block for route')

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
    create_instance_parser.add_argument('-in', '--instance-name', help='Name of the instance')
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


    # Create a parser for the "delete-iam-user" command
    delete_iam_user_parser = subparsers.add_parser('delete-iam-user', help='Delete an IAM user')
    delete_iam_user_parser.add_argument('-un', '--user_name', help='Username of the IAM user')


    # Create a parser for the "create-bucket" command
    create_bucket_parser = subparsers.add_parser('create-bucket', help='Create a bucket')
    create_bucket_parser.add_argument('-bn', '--bucket_name', help='Name of the bucket')
    create_bucket_parser.add_argument('-rg', '--region', help='AWS region')
    create_bucket_parser.add_argument('-f', '--file', help='Path to the YAML file')

    # Create a parser for the "list-bucket" command
    list_bucke_parser = subparsers.add_parser('list-buckets', help='List bucket')

    # Create a parser for the "list-users" command
    list_users_parser = subparsers.add_parser('list-users', help='List IAM users')
    
    # Create a parser for the "list-instances" command
    list_instances_parser = subparsers.add_parser('list-instances', help='List Instances')

    # Create a parser for the "list-vpcs" command
    list_vpcs_parser = subparsers.add_parser('list-vpcs', help='List VPCs')

    # Create a parser for the "delete-bucket" command
    delete_bucket_parser = subparsers.add_parser('delete-bucket', help='Delete a bucket')
    delete_bucket_parser.add_argument('-bn', '--bucket_name', nargs='+', help='Name of the bucket')


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
    # Create commands
    if args['command'] == 'create-instance':
        create_manager.create_instance(args)
    elif args['command'] == 'create-bucket':
        create_manager.create_bucket(args)
    elif args['command'] == 'create-iam-user':
        create_manager.create_iam_user(args)
    elif args['command'] == 'create-iam-role':
        create_manager.create_iam_role(args)
    elif args['command'] == 'create-iam-policy':
        create_manager.create_iam_policy(args)
    
    # Stop commands
    elif args['command'] == 'stop-instance':
        stop_manager.stop_instance(args)
    
    # Delete commands
    elif args['command'] == 'delete-instance':
        delete_manager.delete_instance(args)
    elif args['command'] == 'delete-bucket':
        delete_manager.delete_bucket(args)
    elif args['command'] == 'delete-iam-user':
        delete_manager.delete_iam_user(args)
    
    # List commands
    elif args['command'] == 'list-buckets':
        manager.list_buckets()
    elif args['command'] == 'list-users':
        manager.list_iam_users()
    elif args['command'] == 'list-instances':
        manager.list_instances()
    elif args['command'] == 'list-vpcs':
        manager.list_vpcs()

    # Network commands
    elif args['command'] == 'network':
        if args['action'] == 'create-vpc':
            network_manager.create_vpc(args.get('cidr_block'))
        elif args['action'] == 'create-subnet':
            network_manager.create_subnet(args.get('vpc_id'), args.get('cidr_block'), args.get('availability_zone'))
        elif args['action'] == 'create-internet-gateway':
            network_manager.create_internet_gateway()
        elif args['action'] == 'attach-internet-gateway':
            network_manager.attach_internet_gateway(args.get('vpc_id'), args.get('internet_gateway_id'))
        elif args['action'] == 'create-route-table':
            network_manager.create_route_table(args.vpc_id)
        elif args['action'] == 'create-route':
            network_manager.create_route(args.get('route_table_id'), args.get('destination_cidr_block'), args.get('internet_gateway_id'))
        elif args['action'] == 'associate-subnet-with-route-table':
            network_manager.associate_subnet_with_route_table(args.get('subnet_id'), args.get('route_table_id'))
        elif args['action'] == 'enable-vpc-dns-hostnames':
            network_manager.enable_vpc_dns_hostnames(args.get('vpc_id'))
        else:
            print("Invalid action for 'network' command.")
    # Suggest commands
    elif args['command'] == 'suggest-ami':
        suggest_ami(args)
    
    # Provision commands
    elif args['command'] == 'provision':
        provision(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()