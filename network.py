import boto3

class NetworkManager:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.vpc_client = boto3.client('ec2')

    def create_vpc(self, vpc_name, cidr_block):
        response = self.vpc_client.create_vpc(
            CidrBlock=cidr_block
        )
        vpc_id = response['Vpc']['VpcId']

        self.vpc_client.create_tags(
            Resources=[vpc_id],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': vpc_name
                }
            ]
        )

        print(f"Created VPC with Name: {vpc_name} and ID: {vpc_id}")

    def create_subnet(self, subnet_name, vpc_id, cidr_block, availability_zone):
        response = self.ec2_client.create_subnet(
            VpcId=vpc_id,
            CidrBlock=cidr_block,
            AvailabilityZone=availability_zone
        )
        subnet_id = response['Subnet']['SubnetId']

        self.vpc_client.create_tags(
            Resources=[subnet_id],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': subnet_name
                }
            ]
        )
        print(f"Created subnet with Name: {subnet_name} and ID: {subnet_id}")

    def create_internet_gateway(self):
        response = self.ec2_client.create_internet_gateway()
        internet_gateway_id = response['InternetGateway']['InternetGatewayId']
        print(f"Created internet gateway with ID: {internet_gateway_id}")

    def attach_internet_gateway(self, vpc_id, internet_gateway_id):
        self.ec2_client.attach_internet_gateway(
            VpcId=vpc_id,
            InternetGatewayId=internet_gateway_id
        )
        print(f"Attached internet gateway {internet_gateway_id} to VPC {vpc_id}")

    def create_route_table(self, vpc_id):
        response = self.ec2_client.create_route_table(
            VpcId=vpc_id
        )
        route_table_id = response['RouteTable']['RouteTableId']
        print(f"Created route table with ID: {route_table_id}")

    def create_route(self, route_table_id, destination_cidr_block, gateway_id):
        self.ec2_client.create_route(
            RouteTableId=route_table_id,
            DestinationCidrBlock=destination_cidr_block,
            GatewayId=gateway_id
        )
        print(f"Created route in route table {route_table_id}")

    def associate_subnet_with_route_table(self, subnet_id, route_table_id):
        response = self.ec2_client.associate_route_table(
            SubnetId=subnet_id,
            RouteTableId=route_table_id
        )
        association_id = response['AssociationId']
        print(f"Associated subnet {subnet_id} with route table {route_table_id}")

    def enable_vpc_dns_hostnames(self, vpc_id):
        self.vpc_client.modify_vpc_attribute(
            VpcId=vpc_id,
            EnableDnsHostnames={'Value': True}
        )
        print(f"Enabled DNS hostnames for VPC {vpc_id}")
