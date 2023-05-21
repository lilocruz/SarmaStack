import boto3

class ListManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.iam_client = boto3.client('iam')
        self.ec2_client = boto3.client('ec2')

    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            buckets = response['Buckets']

            if buckets:
                print("List of buckets:")
                for bucket in buckets:
                    bucket_name = bucket['Name']
                    creation_date = bucket['CreationDate']
                    print(f"- {bucket_name} (Created on: {creation_date})")
            else:
                print("No buckets found.")
        except Exception as e:
            print(f"Error occurred while listing buckets: {str(e)}")

    def list_iam_users(self):
        try:
            response = self.iam_client.list_users()
            users = response['Users']

            if users:
                print("List of IAM Users:")
                for user in users:
                    user_name = user['UserName']
                    print(user_name)
            else:
                print("No IAM users found.")
        except Exception as e:
            print(f"Error occurred while listing IAM users: {str(e)}")

    def list_instances(self):
        try:
            response = self.ec2_client.describe_instances()
            reservations = response['Reservations']
            instances = [instance for reservation in reservations for instance in reservation['Instances']]

            if instances:
                print("List of instances:")
                for instance in instances:
                    instance_id = instance['InstanceId']
                    instance_state = instance['State']['Name']
                    print(f"- {instance_id} (Phase: {instance_state})")
            else:
                print("No instances found.")
        except Exception as e:
            print(f"Error occurred while listing instances: {str(e)}")
        
    def list_vpcs(self):
        try:
            response = self.ec2_client.describe_vpcs()
            vpcs = response['Vpcs']
            
            if vpcs:
                print("List of VPCs:")
                for vpc in vpcs:
                    vpc_id = vpc['VpcId']
                    cidr_block = vpc['CidrBlock']
                    state = vpc['State']
                    print(f"- VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}")
            else:
                print("No VPCs found.")
        except Exception as e:
            print(f"Error occurred while listing VPCs: {str(e)}")
    
    def list_subnets(self):
        try:
            response = self.ec2_client.describe_subnets()
            subnets = response['Subnets']
            
            if subnets:
                print("List of Subnets:")
                for subnet in subnets:
                    subnet_id = subnet['SubnetId']
                    vpc_id = subnet['VpcId']
                    cidr_block = subnet['CidrBlock']
                    state = subnet['State']
                    availability_zone = subnet['AvailabilityZone']
                    print(f"- Subnet ID: {subnet_id}, VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}, Availability Zone: {availability_zone}")
            else:
                print("No Subnets found.")
        except Exception as e:
            print(f"Error occurred while listing Subnets: {str(e)}")

    @staticmethod
    def get_location_constraint(region):
        region_mapping = {
            'us-east-1': '',
            'us-east-2': 'us-east-2',
            'us-west-1': 'us-west-1',
            'us-west-2': 'us-west-2',
            'eu-west-1': 'EU',
            # Add more region mappings as needed
        }
        return region_mapping.get(region, region)