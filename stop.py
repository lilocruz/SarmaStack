import boto3

class StopManager:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
    
    def stop_instance(self, args):
        response = self.ec2_client.stop_instances(
            InstanceIds=[args['instance_id']]
    )
        print(f"Stopped EC2 instance with ID: {args['instance_id']}")
