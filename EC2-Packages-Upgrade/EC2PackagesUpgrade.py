import boto3
import csv
import os
from datetime import datetime
import tempfile

bucket = os.getenv("bucket")

def get_instances(ec2):
    return ec2.instances.filter(Filters=[{'Name': 'tag:Environment', 'Values': ['sit',' uat', 'pre', 'dev', 'ft']}])

def update_instance_packages(ssm, instance, command):
    try:
        ssm.send_command(InstanceIds=[instance.id], DocumentName='AWS-RunShellScript', Parameters={'commands': [command]})
        return True
    except ssm.exceptions.InvalidInstanceId:
        return False
    except ssm.exceptions.InvalidDocument:
        return False

def create_temp_csv_file(instances_info):
    with tempfile.NamedTemporaryFile(mode='w', newline='', suffix='.csv', delete=False) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Instance ID', 'Name', 'Command'])
        writer.writerows(instances_info)
        temp_file_name = csvfile.name
    return temp_file_name

def remove_temp_file(temp_file_name):
    os.remove(temp_file_name)
    print(f'Temp file {temp_file_name} removed')

def upload_to_s3(s3, temp_file_name, bucket_name, file_name):
    s3.upload_file(temp_file_name, bucket_name, file_name)

def send_email(ses, recipient, sender, subject, body, temp_file_name):
    with open(temp_file_name, 'rb') as data:
        ses.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}},
            },
            Source=sender
        )

def process_instances(ssm, ec2_client, instances, packages):
    instances_info = []
    for instance in instances:
        ami_id = instance.image_id
        ami_response = ec2_client.describe_images(ImageIds=[ami_id])
        ami_name = ami_response['Images'][0]['Name'] if ami_response['Images'] else ""

        if "ubuntu" in ami_name.lower():
            command = f"sudo apt update && sudo apt upgrade -y {' '.join(packages)}"
        else:
            command = f"sudo yum update -y {' '.join(packages)}"

        name = [tag['Value'] for tag in instance.tags if tag['Key'] == 'Name']
        name = name[0] if name else "N/A"

        if update_instance_packages(ssm, instance, command):
            print(f"Command '{command}' ran successfully on instance id: {instance.id} and name: {name}")
            instances_info.append([instance.id, name, command])
        else:
            print(f"Instance id: {instance.id} and name: {name} failed to run command '{command}', skipping..")

    return instances_info


def lambda_handler(event, context):
    ssm = boto3.client('ssm')
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')
    ses = boto3.client('ses')

    packages = [ # Add list of packages that need updating
        "expat",
        "libcurl",
        "glibc",
        "ntpdate",
        "freetype",
        "curl",
        "zlib",
        "pcre2",
        "runc",
        "kernel",
    ]

    command = f"sudo yum update -y {' '.join(packages)}"
    instances = get_instances(ec2)
    instances_info = process_instances(ssm, ec2_client, instances, packages)

    temp_file_name = create_temp_csv_file(instances_info)

    s3 = boto3.client('s3')
    bucket_name = bucket
    file_name = f'Instances_Updated_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    upload_to_s3(s3, temp_file_name, bucket_name, file_name)
    print(f'File {file_name} uploaded to {bucket_name}')

    recipient = "recipient@youremail.co.uk"
    sender = "sender@youremail.co.uk"
    subject = f'AWS Lambda Vulnerability Execution {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    body = f'The instances that have had the packages updated have been uploaded to the S3 Bucket {bucket_name}'
    send_email(ses, recipient, sender, subject, body, temp_file_name)

    remove_temp_file(temp_file_name)
