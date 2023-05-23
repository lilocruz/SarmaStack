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
    
    def list_iam_roles(self):
        try:
            response = self.iam_client.list_roles()
            roles = response['Roles']

            if roles:
                print("List of IAM Roles:")
                for role in roles:
                    role_name = role['RoleName']
                    print(role_name)
            else:
                print("No IAM roles found.")
        except Exception as e:
            print(f"Error occurred while listing IAM : {str(e)}")
    
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

                    # Retrieve instance tags
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [instance_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    instance_name = tags.get('Name', 'N/A')
                    
                    print(f"- Instance Name: {instance_name}, {instance_id} (Phase: {instance_state})")
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
                    # Retrieve VPC tags
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [vpc_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    vpc_name = tags.get('Name', 'N/A')                
                    
                    print(f"- VPC Name: {vpc_name if vpc_name else 'N/A'}, VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}")
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
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [subnet_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    subnet_name = tags.get('Name', 'N/A')
                    print(f"- Subnet Name: {subnet_name}, Subnet ID: {subnet_id}, VPC ID: {vpc_id}, CIDR Block: {cidr_block}, State: {state}, Availability Zone: {availability_zone}")
            else:
                print("No Subnets found.")
        except Exception as e:
            print(f"Error occurred while listing Subnets: {str(e)}")   
    
    def list_route_tables(self):
        try:
            response = self.ec2_client.describe_route_tables()
            route_tables = response['RouteTables']

            if route_tables:
                print("List of Route Tables:")
                for route_table in route_tables:
                    route_table_id = route_table['RouteTableId']
                    vpc_id = route_table['VpcId']
                    routes = route_table['Routes']
                    associations = route_table['Associations']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [route_table_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    route_tables_name = tags.get('Name', 'N/A')
                    print(f"- Route Table Name: {route_tables_name}, Route Table ID: {route_table_id}, VPC ID: {vpc_id}")
                    print("  Routes:")
                    for route in routes:
                        destination_cidr_block = route.get('DestinationCidrBlock')
                        gateway_id = route.get('GatewayId')
                        if destination_cidr_block and gateway_id:
                            print(f"    Destination: {destination_cidr_block}, Gateway ID: {gateway_id}")
                    print("  Associations:")
                    for association in associations:
                        subnet_id = association.get('SubnetId')
                        main = association.get('Main')
                        if subnet_id:
                            print(f"    Subnet ID: {subnet_id}, Main: {main}")
            else:
                print("No Route Tables found.")
        except Exception as e:
            print(f"Error occurred while listing Route Tables: {str(e)}")

    def list_internet_gateways(self):
        try:
            response = self.ec2_client.describe_internet_gateways()
            internetgateways = response['InternetGateways']

            if internetgateways:
                print("List of Internet Gateways:")
                for internetgateway in internetgateways:
                    internetgateway_id = internetgateway['InternetGatewayId']
                    tags_response = self.ec2_client.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [internetgateway_id]}])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    internetgateway_name = tags.get('Name', 'N/A')
                    print(f"- Internet Gateway Name: {internetgateway_name}, Internet Gateway ID: {internetgateway_id}")
            else:
                print("No Internet Gateway found.")
        except Exception as e:
            print(f"Error occured while listing Internet Gateway: {str(e)}")

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