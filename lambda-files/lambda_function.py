import json
import boto3
import os
import uuid
import logging
import re

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Predefined skills list
SKILLS_LIST = ['AWS', 'Python', 'Terraform', 'Java', 'JavaScript', 'DevOps', 'Kubernetes', 'SQL', 'Linux']

def detect_skills(text, skills_list):
    """ Detect skills from the predefined list. """
    return [skill for skill in skills_list if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]

def extract_experience(text):
    """ Extracts years of experience from the text. """
    match = re.search(r'(\d+)\s*(?:year|yr|years)', text, re.IGNORECASE)
    return match.group(1) if match else 'Not found'

def extract_name(text):
    """ Improved regex to extract full names with proper capitalization. """
    match = re.search(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)\b', text)
    return match.group(1).strip() if match else 'Not found'

def extract_email(text):
    """ Extracts email addresses from the text. """
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else 'Not found'

def extract_skills_with_comprehend(text):
    """ Extracts skills using AWS Comprehend. """
    try:
        comprehend_client = boto3.client('comprehend')
        response = comprehend_client.detect_entities(Text=text, LanguageCode='en')
        return [entity['Text'] for entity in response.get('Entities', []) if entity['Type'] == 'SKILL']
    except Exception as e:
        logger.error(f"Comprehend error: {str(e)}")
        return []

def lambda_handler(event, context):
    """ AWS Lambda handler for processing resumes using Textract and storing details in DynamoDB. """
    s3_client = boto3.client('s3')
    textract_client = boto3.client('textract')
    dynamodb = boto3.resource('dynamodb')

    bucket_name = os.environ.get('S3_BUCKET')
    table_name = os.environ.get('DDB_TABLE')
    table = dynamodb.Table(table_name)

    if 'Records' not in event:
        logger.error("Invalid event format: No 'Records' found")
        return {'statusCode': 400, 'body': json.dumps("Invalid event format")}

    for record in event['Records']:
        file_name = record['s3']['object']['key']
        logger.info(f"Processing file: {file_name}")

        try:
            # Ensure file exists before processing
            s3_client.head_object(Bucket=bucket_name, Key=file_name)
            
            response = textract_client.analyze_document(
                Document={'S3Object': {'Bucket': bucket_name, 'Name': file_name}},
                FeatureTypes=['FORMS']
            )

            # Extract text content
            text_blocks = [block.get('Text', '') for block in response.get('Blocks', []) if block.get('BlockType') == 'WORD']
            extracted_text = " ".join(text_blocks)

            if not extracted_text.strip():
                logger.warning("No text extracted from the document.")
                return {'statusCode': 400, 'body': json.dumps("No text found in the document.")}

            logger.info(f"Extracted Text Sample: {extracted_text[:500]}...")

            # Extract details
            candidate_name = extract_name(extracted_text)
            experience = extract_experience(extracted_text)
            email = extract_email(extracted_text)
            skills = detect_skills(extracted_text, SKILLS_LIST)
            skills += extract_skills_with_comprehend(extracted_text)

            # Ensure skills are unique
            skills = list(set(skills)) if skills else ['Not found']

            logger.info(f"Extracted Name: {candidate_name}")
            logger.info(f"Extracted Experience: {experience}")
            logger.info(f"Extracted Email: {email}")
            logger.info(f"Extracted Skills: {skills}")

            # Store in DynamoDB
            resume_id = str(uuid.uuid4())
            table.put_item(
                Item={
                    'ResumeID': resume_id,
                    'CandidateName': candidate_name,
                    'Skills': skills,
                    'Experience': experience,
                    'ContactEmail': email
                }
            )

        except boto3.exceptions.Boto3Error as boto_err:
            logger.error(f"AWS Error processing file {file_name}: {str(boto_err)}")
            return {'statusCode': 500, 'body': json.dumps(f"AWS Error: {str(boto_err)}")}
        except Exception as e:
            logger.error(f"General Error processing file {file_name}: {str(e)}")
            return {'statusCode': 500, 'body': json.dumps(f"Error: {str(e)}")}

    return {'statusCode': 200, 'body': json.dumps('Resume processed successfully!')}
