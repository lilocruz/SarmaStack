import yaml
from state import StateTracker
from create import CreateManager

def provision(args):
    state_tracker = StateTracker()
    create_manager = CreateManager()

    with open(args['file'], 'r') as f:
        data = yaml.safe_load(f)

    if 'instances' in data:
        instances = data['instances']
        for instance in instances:
            instance_name = instance.get('instance_name')
            if not state_tracker.resource_exists('instances', instance_name):
                if args.get('build'):
                    print(f"Would create instance: {instance_name}")
                else:
                    create_manager.create_instance(instance)
                    state_tracker.update_resource_state('instances', instance_name, {})
            else:
                print(f"Instance '{instance_name}' already exists. Skipping creation.")

    if 'buckets' in data:
        buckets = data['buckets']
        for bucket in buckets:
            bucket_name = bucket.get('bucket_name')
            if not state_tracker.resource_exists('buckets', bucket_name):
                if args.get('build'):
                    print(f"Would create bucket: {bucket_name}")
                else:
                    create_manager.create_bucket(bucket)
                    state_tracker.update_resource_state('buckets', bucket_name, {})
            else:
                print(f"Bucket '{bucket_name}' already exists. Skipping creation.")

    if 'resources' in data:
        resources = data['resources']
        for resource in resources:
            resource_type = resource.get('type')
            resource_name = resource.get('name')
            if resource_type == 'iam_user':
                if not state_tracker.resource_exists('iam_users', resource_name):
                    if args.get('build'):
                        print(f"Would create IAM user: {resource_name}")
                    else:
                        create_manager.create_iam_user(resource)
                        state_tracker.update_resource_state('iam_users', resource_name, {})
                else:
                    print(f"IAM user '{resource_name}' already exists. Skipping creation.")
            elif resource_type == 'iam_role':
                if not state_tracker.resource_exists('iam_roles', resource_name):
                    if args.get('build'):
                        print(f"Would create IAM role: {resource_name}")
                    else:
                        role_name = resource.get('role_name')
                        assume_role_policy = resource.get('assume_role_policy')
                        create_manager.create_iam_role(role_name, assume_role_policy)
                        state_tracker.update_resource_state('iam_roles', resource_name, {})
                else:
                    print(f"IAM role '{resource_name}' already exists. Skipping creation.")
            elif resource_type == 'iam_policy':
                if not state_tracker.resource_exists('iam_policies', resource_name):
                    if args.get('build'):
                        print(f"Would create IAM policy: {resource_name}")
                    else:
                        create_manager.create_iam_policy(resource)
                        state_tracker.update_resource_state('iam_policies', resource_name, {})
                else:
                    print(f"IAM policy '{resource_name}' already exists. Skipping creation.")
            else:
                print(f"Unsupported resource type: {resource_type}")

    state_tracker.save_state()