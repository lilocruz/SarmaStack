import boto3
import yaml

class DeleteManager:
    def delete_instance(self, args):
        if args.get('file'):
            with open(args['file'], 'r') as f:
                data = yaml.safe_load(f)
                instances = data.get('instances')
                if instances:
                    instance_ids = [instance['instance_id'] for instance in instances]
                    self.delete_instance({'instance_ids': instance_ids})
                else:
                    print("No instance specifications found in the YAML file.")
        else:
            ec2_client = boto3.client('ec2')
            instance_ids = args.get('instance_ids')
            if instance_ids:
                response = ec2_client.terminate_instances(InstanceIds=instance_ids)
                print(f"Deleted instances: {args['instance_ids']}")
    
    def delete_bucket(self, args):
        s3_client = boto3.client('s3')

        bucket_names = args.get('bucket_name')

        if bucket_names:
            for bucket_name in bucket_names:
                try:
                    s3_client.delete_bucket(Bucket=bucket_name)
                    print(f"Deleted bucket {bucket_name}")
                except Exception as e:
                    print(f"Error occurred while deleting bucket {bucket_name}: {str(e)}")
        else:
            print("Please provide the 'bucket_names' argument with a list of bucket names to delete.")

    def delete_iam_user(self, args):
        iam_client = boto3.client('iam')
        user_name = args.get('user_name')

        if user_name:
            try:
                response = iam_client.delete_user(UserName=user_name)
                print(f"Deleted IAM user: {user_name}")
            except Exception as e:
                print(f"Error occurred while deleting IAM user: {str(e)}")
        else:
            print("Please provide the 'user_name' argument.")
    
    def delete_iam_role(self, args):
        iam_client = boto3.client('iam')
        role_name = args.get('role_name')

        if role_name:
            try:
                response = iam_client.delete_role(RoleName=role_name)
                print(f"Deleted IAM role: {role_name}")
            except Exception as e:
                print(f"Error occurred while deleting IAM roles: {str(e)}")
        else:
            print("Please provide the 'role_name' argument.")
    
    def delete_vpc(self, args):
        ec2_client = boto3.client('ec2')
        vpc_id = args.get('vpc_id')

        if vpc_id:
            try:
                response = ec2_client.delete_vpc(VpcId=vpc_id)
                print(f"Deleted VPC: {vpc_id}")
            except Exception as e:
                print(f"Error occurred while deleting VPC: {str(e)}")
        else:
            print("Please provide the 'vpc_id' argument.")
    
    def delete_subnet(self, args):
        ec2_client = boto3.client('ec2')
        subnet_id = args.get('subnet_id')

        if subnet_id:
            try:
                response = ec2_client.delete_subnet(SubnetId=subnet_id)
                print(f"Delete Subnet: {subnet_id}")
            except Exception as e:
                print(f"Error occured while deleting Subnet: {str(e)}")
        else:
            print("Please provide the 'subnet_id' argument.")
    
    def delete_route_table(self, args):
        ec2_client = boto3.client('ec2')
        route_table_id = args.get('route_table_id')

        if route_table_id:
            try:
                response = ec2_client.delete_route_table(RouteTableId=route_table_id)
                print(f"Delted Route Table: {route_table_id}")
            except Exception as e:
                print(f"Error occured while deleting Route Table: {str(e)}")
        else:
            print("Please provide the 'route_table_id' argument.")

    def delete_internet_gateway(self, args):
        ec2_client = boto3.client('ec2')
        internet_gateay_id = args.get('internet_gateway_id')

        if internet_gateay_id:
            try:
                response = ec2_client.delete_internet_gateway(InternetGatewayId=internet_gateay_id)
                print(f"Deleted Internet Gateway: {internet_gateay_id}")
            except Exception as e:
                print(f"Error occurdd while deleting Internet Gateway: {str(e)}")
        else:
            print("Please provide the 'internet_gateway_id' argument.")