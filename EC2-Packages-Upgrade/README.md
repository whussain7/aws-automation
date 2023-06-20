# EC2 Instances Automation

## Table of Contents
1. [Overview](#Overview)
2. [Features](#Features)
3. [Prerequisites](#Prerequisites)
4. [Installation](#Installation)
5. [Usage](#Usage)
6. [Contributing](#Contributing)

## Overview
This project automates the process of updating software packages in AWS EC2 instances across multiple environments using Python, Boto3, and AWS Lambda. This helps to streamline your AWS management workflow, maintain the security of your instances, and save time on administrative tasks.

## Features
- Automatically filter EC2 instances based on the 'Environment' tag.
- Update the software packages of the filtered instances.
- Create a report in CSV format of the instances updated.
- Upload the report to a specified S3 bucket.
- Send an email notification with the report attached.
- Clean up temporary files used in the process.


## Prerequisites
- ![Python versions](https://img.shields.io/badge/Python-3.6%20|%203.7%20|%203.8%20|%203.9|%203.10|%203.11-blue)
- AWS account and CLI configured with the required access rights.
- An AWS S3 bucket.
- An AWS SES configured for sending email notifications.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/aws-ec2-instances-automation
2. Create a Virtual Environment:
    ```bash
    python3 -m venv
3. Active Virtual Environment
    ```bash
    source <my_env_name>/bin/activate
4. Install dependencies using pip:
    ```bash
    pip install -r requirements.txt

## Usage
This project is designed to be deployed as an AWS Lambda function, which can be manually triggered or set to execute on a daily schedule using EventBridge. Alternatively, it can be adapted to run directly on an EC2 instance as a cron job.

- Ensure that your AWS CLI is configured correctly.
- Set up an AWS S3 bucket for storing the report CSV file.
- Set up AWS SES for sending email notifications, in a sandbox environment its free.
- Deploy the function to AWS Lambda.
- Manually trigger the function or set it to execute on a daily schedule with EventBridge.
- If desired, adapt the script to run as a cron job using crontab directly on an EC2 instance.

## Contribution
I appreciate your contributions, follow the guidelines set out below by GitHub for any PRs or improvements you may think could work further with this script:

- Fork the Project
- Create your Feature Branch (git checkout -b feature/AmazingFeature)
- Commit your Changes (git commit -m 'Add some AmazingFeature')
- Push to the Branch (git push origin feature/AmazingFeature)
- Open a Pull Request

## Like the Project?
- Ensure to Star it: [AWS Automation](https://github.com/whussain7/aws-automation)

## Connect with me?

Hit me up below on:
- [LinkedIn Profile](https://www.linkedin.com/in/wahab-hussain-479543182/)
- [GitHub Profile](https://github.com/whussain7)

