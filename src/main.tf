provider "aws" {
  region = "us-east-1" # Change as needed
}

# S3 Bucket for Resume Storage
resource "aws_s3_bucket" "resume_bucket" {
  bucket = "ai-resume-screening-bucket"
}

# DynamoDB Table for Storing Extracted Resume Data
resource "aws_dynamodb_table" "resume_table" {
  name           = "ResumeData"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ResumeID"

  attribute {
    name = "ResumeID"
    type = "S"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_ai_resume_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# IAM Policy for Textract, Comprehend, S3, DynamoDB, and CloudWatch Logs
resource "aws_iam_policy" "lambda_policy" {
  name        = "LambdaAIResumePolicy"
  description = "Policy for Lambda to access AI services and CloudWatch Logs"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "textract:DetectDocumentText",
        "textract:AnalyzeDocument",
        "comprehend:DetectEntities",
        "comprehend:DetectKeyPhrases",
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:PutItem"],
      "Resource": "${aws_dynamodb_table.resume_table.arn}"
    },
    {
      "Effect": "Allow",
      "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
      "Resource": "*"
    }
  ]
}
EOF
}

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "lambda_policy_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Lambda Function
resource "aws_lambda_function" "resume_processor" {
  function_name = "ResumeProcessor"
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda_role.arn

  filename         = "lambda_function.zip" # Ensure this file is built and uploaded
  source_code_hash = filebase64sha256("lambda_function.zip")

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.resume_bucket.bucket
      DDB_TABLE = aws_dynamodb_table.resume_table.name
    }
  }
}

# S3 Event Trigger for Lambda
resource "aws_s3_bucket_notification" "s3_trigger" {
  bucket = aws_s3_bucket.resume_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.resume_processor.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

# Grant S3 Permission to Invoke Lambda
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowS3InvokeLambda"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resume_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.resume_bucket.arn
}

