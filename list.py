import boto3
from tabulate import tabulate 

class ListManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.iam_client = boto3.client('iam')
        self.ec2_client = boto3.client('ec2')

    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            buckets = response['Buckets']
            table_data = []

            if buckets:
                for bucket in buckets:
                    bucket_name = bucket['Name']
                    creation_date = bucket['CreationDate']
                    table_data.append([bucket_name, creation_date])
                    
                headers = ['Bucket Name', 'Creation Date']
                print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            else:
                print("No buckets found.")
        except Exception as e:
            print(f"Error occurred while listing buckets: {str(e)}")

    def list_iam_users(self):
        try:
            response = self.iam_client.list_users()
            users = response['Users']
            table_data = []
            
            if users:
                for user in users:
                    user_name = user['UserName']
                    table_data.append([user_name])
                
                headers = ['User Name']
                print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            else:
                print("No IAM users found.")
        except Exception as e:
            print(f"Error occurred while listing IAM users: {str(e)}")
    
    def list_iam_roles(self):
        try:
            response = self.iam_client.list_roles()
            roles = response['Roles']
            table_data = []

            if roles:
                for role in roles:
                    role_name = role['RoleName']
                    table_data.append([role_name])
                
                headers = ['Role Name']
                print(tabulate(table_data, headers, tablefmt='fancy_grid'))
            else:
                print("No IAM roles found.")
        except Exception as e:
            print(f"Error occurred while listing IAM : {str(e)}")
    
    def list_instances(self):
        response = self.ec2_client.describe_instances()
        instances = response['Reservations']
        table_data = []

        if instances:
            for reservation in instances:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    instance_type = instance['InstanceType']
                    state = instance['State']['Name']
                    launch_time = instance['LaunchTime'].strftime('%Y-%m-%d %H:%M:%S')
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    instance_name = tags.get('Name', 'N/A')
                    table_data.append([instance_name, instance_id, instance_type, state, launch_time])
                    headers = ['Instance Name', 'Instance ID', 'Instance Type', 'State', 'Launch Time']
                    print(tabulate(table_data, headers, tablefmt="fancy_grid"))
        else:
            print("No instances found.")
        
    def list_vpcs(self):
        try:
            response = self.ec2_client.describe_vpcs()
            vpcs = response['Vpcs']
            table_data = []
            
            if vpcs:
                for vpc in vpcs:
                    vpc_id = vpc['VpcId']
                    cidr_block = vpc['CidrBlock']
                    state = vpc['State']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    vpc_name = tags.get('Name', 'N/A')                
                    table_data.append([vpc_name, vpc_id, cidr_block, state])
                
                headers = ['Name', 'ID', 'Cidr Block', 'State']
                print(tabulate(table_data, headers, tablefmt='fancy_grid'))
            else:
                print("No VPCs found.")
        except Exception as e:
            print(f"Error occurred while listing VPCs: {str(e)}")
    
    def list_subnets(self):
        try:
            response = self.ec2_client.describe_subnets()
            subnets = response['Subnets']
            table_data = []
            
            if subnets:
                for subnet in subnets:
                    subnet_id = subnet['SubnetId']
                    vpc_id = subnet['VpcId']
                    cidr_block = subnet['CidrBlock']
                    state = subnet['State']
                    availability_zone = subnet['AvailabilityZone']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [subnet_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    subnet_name = tags.get('Name', 'N/A')
                    table_data.append([subnet_name, subnet_id, vpc_id, cidr_block, availability_zone, state])
                
                headers = ['Name', 'ID', 'VPC ID', 'Cidr Block', 'Availability Zone', 'State']
                print(tabulate(table_data, headers, tablefmt='fancy_grid'))
            else:
                print("No Subnets found.")
        except Exception as e:
            print(f"Error occurred while listing Subnets: {str(e)}")   
    
    def list_route_tables(self):
        try:
            response = self.ec2_client.describe_route_tables()
            route_tables = response['RouteTables']
            table_data = []
            
            if route_tables:
                for route_table in route_tables:
                    route_table_id = route_table['RouteTableId']
                    vpc_id = route_table['VpcId']
                    routes = route_table['Routes']
                    associations = route_table['Associations']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [route_table_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    route_table_name = tags.get('Name', 'N/A')
                    
                    table_data.append([route_table_name, route_table_id, vpc_id])
                    
                    for route in routes:
                        destination_cidr_block = route.get('DestinationCidrBlock')
                        gateway_id = route.get('GatewayId')
                        if destination_cidr_block and gateway_id:
                            table_data.append(["", destination_cidr_block, gateway_id])
                            
                            for association in associations:
                                subnet_id = association.get('SubnetId')
                                main = association.get('Main')
                                if subnet_id:
                                    table_data.append(["", f"Subnet ID: {subnet_id}", f"Main: {main}"])

                headers = ['Route Table Name', 'Route Table ID & Destination', 'VPC ID & Target']
                print(tabulate(table_data, headers, tablefmt="fancy_grid"))
            else:
                print("No Route Tables found.")
        except Exception as e:
            print(f"Error occurred while listing Route Tables: {str(e)}")
    
    def list_internet_gateways(self):
        try:
            response = self.ec2_client.describe_internet_gateways()
            internetgateways = response['InternetGateways']
            table_data = []

            if internetgateways:
                for intertgateway in internetgateways:
                    internetgateway_id = intertgateway['InternetGatewayId']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [internetgateway_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    internetgateway_name = tags.get('Name', 'N/A')
                    table_data.append([internetgateway_name, internetgateway_id])
                
                headers = ['Name', 'ID']
                print(tabulate(table_data, headers, tablefmt='fancy_grid'))
            else:
                print("No Internet Gateways Found.")
        except Exception as e:
            print(f"Error occured while listing Internet Gateways: {str(e)}")


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