# poc-jira-langchain-bedrock
A simple project that shows how to integrate Jira+AWS+AnthropicClaude to autonomously reply to client's support requests.

![Agent Architecture](/mermaid/architecture.png)

In the following, you can find the Step-to-Step to deploy.

# Step-to-step to Deploy
1. [JIRA] Go to JIRA and create your account;
2. [JIRA] Configure an API token, so you can access your board and manage the cards: https://id.atlassian.com/manage-profile/security/api-tokens;
3. [AWS] Create a MySQL RDS instance. Set up the credentials as the same in the lambda_function.py file, inside the /aws/lambda_function.zip package;
4. [AWS] Connect to the created RDS and run the SQL commands available at /sql/database_dump.sql;
5. [AWS] Configure the Security Group attached to the RDS to allow traffic from different VPCs. To do so, configure the source of both inbound/outbound rules of the attached VPC to be 0.0.0.0/0 at least for port 3306. If this step is not properlly configured, your Lambda will not be able to connect to Bedrock later;
6. [AWS] Configure an AWS Bedrock FM, to use Claude Sonnet 4.6, as we can see in this image ![Bedrock FM](/aws/bedrock-foundational-model.png)
7. [AWS] Create an AWS Lambda Python, and upload the /aws/lambda_function.zip package as its code;
8. [AWS] Adjust environment and credentials in your Lambda code (JIRA token, database credentials, etc);
9. [AWS] Configure a FunctionURL to your Lambda, so it can be triggered by URL;
10. [JIRA] Setup a JIRA webhook, to be triggered when you create a JIRA card: https://<YOUR_SITE>.atlassian.net/plugins/servlet/webhooks;
11. [JIRA] Open your board at https://<YOUR_SITE>.atlassian.net/jira/software/projects/KAN/boards/1 and create a card. In the card description, place the following: "Show me which records in the users table have gender = male.";
13. [AWS/JIRA] FuP your request in CloudWatch and get your response in the card as a comment.
