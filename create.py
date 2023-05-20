import boto3
import json
import yaml
import botocore.exceptions

class CreateManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.ec2_client = boto3.client('ec2')
        self.iam_client = boto3.client('iam')
    
    def create_instance(self, args):
        if args.get('file'):
            with open(args['file'], 'r') as f:
                data = yaml.safe_load(f)
                instances = data.get('instances')
                if instances:
                    for instance in instances:
                        self.create_instance(instance)
                else:
                    print("No instance specifications found in the YAML file.")

        else:
            instance_name = args.get('instance_name') or 'default-name'  # Use a default name if not provided
            response = self.ec2_client.run_instances(
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
                                'Value': instance_name or ''
                            },
                        ]
                    },
                ]
            )
            print(f"Created instance with id {args['image_id']} and name: {args['instance_name']}")

    def create_bucket(self, args):
        bucket_name = args.get('bucket_name')
        region = args.get('region')

        if bucket_name and region:
            location_constraint = self.get_location_constraint(region)

            try:
                if location_constraint:
                    response = self.s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': location_constraint
                        }
                    )
                else:
                    response = self.s3_client.create_bucket(Bucket=bucket_name)

                print(f"Created bucket {bucket_name} in region {region}")
            except botocore.exceptions.ClientError as e:
                error_code = e.response['Error']['Code']
                error_message = e.response['Error']['Message']
                if error_code == 'BucketAlreadyExists':
                    print(f"Bucket {bucket_name} already exists.")
                else:
                    print(f"Error occurred while creating the bucket: {error_message}")
            except Exception as e:
                print(f"Error occurred while creating the bucket: {str(e)}")
        else:
            print("Please provide both 'bucket_name' and 'region' arguments.")

    def create_iam_user(self, args):
        response = self.iam_client.create_user(
            UserName=args['user_name']
        )
        print(f"Created IAM user: {args['user_name']}")

    def create_iam_role(self, resource):
        role_name = resource.get('role_name')
        assume_role_policy = resource.get('assume_role_policy')

        if role_name and assume_role_policy:
            try:
                response = self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=json.dumps(assume_role_policy)
                )
                print(f"Created IAM role {role_name}")
            except Exception as e:
                print(f"Error occurred while creating IAM role {role_name}: {str(e)}")
        else:
            print("Please provide both 'role_name' and 'assume_role_policy' arguments.")

    def create_iam_policy(self, args):
        with open(args['policy_document'], 'r') as f:
            policy_document = f.read()
        response = self.iam_client.create_policy(
            PolicyName=args['policy_name'],
            PolicyDocument=policy_document
        )
        print(f"Created IAM policy: {args['policy_name']}")

    def get_location_constraint(self, region):
        if region == 'us-east-1':
            return ''
        else:
            return region
