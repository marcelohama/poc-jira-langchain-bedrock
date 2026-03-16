# poc-jira-langchain-bedrock
A simple project that shows how to integrate Jira+AWS+AnthropicClaude to autonomously reply to client's support requests.

![Agent Architecture](/mermaid/architecture.png)

# Step-to-Step to Deploy
1. Go to JIRA and create your account;
2. Configure an API token, so you can access your board and manage the cards: https://id.atlassian.com/manage-profile/security/api-tokens
3. Configure an AWS Bedrock FM, to use Claude Sonnet 4.6, as we can see in this image ![Bedrock FM](/aws/bedrock-foundational-model.png)
