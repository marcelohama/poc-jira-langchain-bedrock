import pymysql.cursors
import json
import boto3
import requests
from requests.auth import HTTPBasicAuth

# --- Configuration (using environment variables for security) ---
DB_HOST = '<MYSQL_RDS_HOST>'
DB_USER = '<MYSQL_RDS_USER>'
DB_PASS = '<MYSQL_RDS_PASS>'
DB_NAME = '<MYSQL_RDS_DBNAME>'
USER_EMAIL = 'JIRA_USER_EMAIL'
JIRA_URL = 'JIRA_SITE_URL'
JIRA_TK = '<JIRA_TOKEN>'

def lambda_handler(event, context):
    
    # 1. Extract JIRA data, posted by client
    body = json.loads(event['body'])
    issue_key = body['issue']['key']
    event_type = body['webhookEvent']
    description = body['issue']['fields']['description']
    print(f"Card {issue_key} disparou evento: {event_type} com descricao {description}")
    
    # 2. Initialize the Bedrock runtime client
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-2')
    # Define model ID and used schema
    model_id = "global.anthropic.claude-sonnet-4-6"
    db_schema = """
        Table: users
        Columns: id (INT), first_name (VARCHAR), last_name (VARCHAR), email (VARCHAR), gender (VARCHAR)
    """
    # 3. Natural Language Query and Prompt with context
    user_question = description
    prompt = f"""
        Given the following database schema: {db_schema}
        Generate a SQL query to answer the following question: {user_question}
        Provide only the SQL query, no explanation.
    """
    # 4. Converse API Call
    messages = [{
        "role": "user",
        "content": [{"text": prompt}]
    }]
    # 5. Build SQL query with Bedrock LN2SQL capabilities
    generated_sql = ''
    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={"maxTokens": 500, "temperature": 0}
        )
        generated_sql = response["output"]["message"]["content"][0]["text"].lower()
        generated_sql = generated_sql.replace("```sql", "").replace("```", "")
        generated_sql = generated_sql.replace("```sql", "").replace("\n```", "")
        print("Generated SQL:", generated_sql)
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error invoking model')
        }
    
    # 6. Establish a database connection
    result = "empty"
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:    
            cursor.execute(generated_sql)
            result = cursor.fetchall()
            print("Generated Result: ", result)
    except pymysql.MySQLError as e:
        print(f"ERROR: Could not connect to MySQL instance: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Database connection failed')
        }
    finally:
        connection.close() # Always close the connection
        print("Database connection closed")    
    
    # 7. Issue key and comment body
    if result != "empty":
        url = f"{JIRA_URL}/rest/api/2/issue/{issue_key}/comment"
        auth = HTTPBasicAuth(USER_EMAIL, JIRA_TK)
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        
        prompt = f"""
            You are a jira agent assistant, expert in customer relationship.
            Answer to the following customer question in plain text: "{user_question}",
            using the following json as result data: "{result}",
            considering that the client don't understands technology,
            and also considering that the answer will be a comment in jira card.
        """
        messages = [{
            "role": "user",
            "content": [{"text": prompt}]
        }]
        generated_response = ''
        try:
            response = bedrock_runtime.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={"maxTokens": 500, "temperature": 0}
            )
            generated_response = response["output"]["message"]["content"][0]["text"].lower()
            print("Generated Response:", generated_response)
        except Exception as e:
            print(e)
            return {
                'statusCode': 500,
                'body': json.dumps('Error invoking model')
            }
        
        payload = json.dumps({"body": generated_response}, indent=4)
        response = requests.post(url, data=payload, headers=headers, auth=auth)
        if response.status_code == 201:
            print("Comment posted successfully!")
        else:
            print(f"Failed to post comment. Status code: {response.status_code}, Response: {response.text}")
        return {
            'statusCode': 200,
            'body': json.dumps('Operation successful')
        }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps('Debrock agent could not resolve to a valid query.')
        }