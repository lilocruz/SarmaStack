# SarmaStack

SarmaStack is an Infrastructure as Code (IaC) tool designed to simplify the provisioning and management of AWS cloud infrastructure resources. With SarmaStack, you can define your AWS infrastructure configurations in a declarative manner and easily create and manage your resources.

https://sarmastack.com/

## Features

- YAML for defining infrastructure resources
- Integration with AWS services through Boto3
- CLI for managing and provisioning infrastructure resources
- Suggestion feature to recommend AMI image IDs based on specified criteria

## Installation

1. Clone the SarmaStack repository:

```bash
git clone https://github.com/your-username/sarmastack.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Suggesting AMI image IDs

To suggest AMI image IDs based on specified criteria, use the following command:

```python
python sarmastack.py suggest-ami --filter-name <filter_name> --filter-values <filter_values>
```

Example:

```python
python sarmastack.py suggest-ami --filter-name name --filter-values ubuntu
```

### 2. Creating an EC2 Instance

To create an EC2 instance, use the following command:

```python
python sarmastack.py create-instance <instance_name> --instance-type <instance_type> --image-id <image_id>
```

Example:

```python
python sarmastack.py create-instance my-instance --instance-type t2.micro --image-id ami-12345678
```

### 3. Creating an S3 Bucket

To create an S3 bucket, use the following command:

```python
python sarmastack.py create-bucket <bucket_name>
```

Example:

```python
python sarmastack.py create-bucket my-bucket
```


### 4. Provisioning Infrastructure from YAML File

To provision infrastructure resources from a YAML file, use the following command:

python sarmastack.py provision <file_path>


Example:

```python
python sarmastack.py provision infrastructure.yaml
```


## Contributing

Contributions to SarmaStack are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the `GPLv3` License. 


