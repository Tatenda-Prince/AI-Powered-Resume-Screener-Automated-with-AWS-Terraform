# AI-Powered-Resume-Screener-Automated-with-AWS-Terraform

"Screening Through Resumes"

# Technical Architecture

![image_alt]()

## Project Overview

This project automates the HR recruitment process by using AWS AI services to analyze resumes. It extracts skills and experience from resumes and stores the results for recruiters to review.

## Project Objective 

1.Extracting text from resumes using AWS Textract

2.Identifying key skills & experience using AWS Comprehend

3.Storing structured candidate data in Amazon DynamoDB

4.Providing an efficient & scalable solution using AWS Lambda & S3


## Features

1.Automated Resume Processing: Upload resumes to Amazon S3.

2.Text Extraction: Uses AWS Textract to extract text from resumes.

3.Skill & Experience Analysis: AWS Comprehend identifies key skills like AWS, Python, DevOps, etc.

4.Data Storage: Stores analyzed data in Amazon DynamoDB.

5.Serverless Architecture: Built with AWS Lambda, ensuring scalability.

6.Infrastructure as Code: Deployed using Terraform.


## Technology Used

1.AWS Services: S3, Textract, Comprehend, Lambda, DynamoDB

2.Infrastructure: Terraform

3.Languages: Python (Lambda functions)

4.Testing: AWS CLI


## Prerequisites

1.Personal AWS account with basic understanding of AWS and Python

2.AWS CLI configured with the required permissions

3.Terraform installed on your local machine


## Step 1: Clone the Repository

1.1.Clone this repository to your local machine

```python
git clone https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform.git

```

## Step 2 : Run Terraform workflow to initialize, validate, plan then apply

2.1.In your local terraform visual code environment terminal, to initialize the necessary providers, execute the following command in your environment terminal —

```json

Terraform init

```

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform/blob/13137591852601f834fb477da5d85204830d5206/img/Screenshot%202025-02-16%20203301.png)


Upon completion of the initialization process, a successful prompt will be displayed, as shown below.


2.2.Next, let’s ensure that our code does not contain any syntax errors by running the following command —

```json

Terraform validate

```

The command should generate a success message, confirming that it is valid, as demonstrated below.

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform/blob/fde661d4e2e2639aaa061d50bd28f55859ba2372/img/Screenshot%202025-02-16%20203327.png)

2.3.Let’s now execute the following command to generate a list of all the modifications that Terraform will apply. —


```json

Terraform plan

```

![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform/blob/fad3bb31fb9e1848ff22819f325e55287af243c8/img/Screenshot%202025-02-16%20203405.png)

The list of changes that Terraform is anticipated to apply to the infrastructure resources should be displayed. The “+” sign indicates what will be added, while the “-” sign indicates what will be removed.


2.4.Now, let’s deploy this infrastructure! Execute the following command to apply the changes and deploy the resources.

Note — Make sure to type “yes” to agree to the changes after running this command


```json

Terraform apply

```

Terraform will initiate the process of applying all the changes to the infrastructure. Kindly wait for a few seconds for the deployment process to complete.


![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform/blob/9db4af2d48a621cebbd3a3cea5e4203f90b9c9a2/img/Screenshot%202025-02-16%20203621.png)


## Success!

The process should now conclude with a message indicating “Apply complete”, stating the total number of added, modified, and destroyed resources, accompanied by several resources.


![image_alt](https://github.com/Tatenda-Prince/AI-Powered-Resume-Screener-Automated-with-AWS-Terraform/blob/a65dc0dc27d848b159ba7a0b06336eef5f9984b8/img/Screenshot%202025-02-16%20203648.png)


## Step 3: Verify creation of AWS Lambda, Amazon S3 and DynamoDB






