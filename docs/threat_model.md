# Threat Model for RAGShield

## Assets
- Documents
- User Data
- Vector Database
- LLM
- System Prompt
- Access Policies

## Threats
- **Direct Prompt Injection**: User attempting to override LLM instructions.
- **Indirect Prompt Injection**: Malicious text inside a retrieved document altering the LLM's behavior.
- **Unauthorized Retrieval**: Users attempting to retrieve documents they do not have access to.
- **Data Leakage**: The LLM accidentally leaking sensitive data it has seen during generation.

## Controls
- **Prompt Scanner**: Analyzes incoming queries for known injection keywords.
- **Document Scanner**: Scans retrieved documents for embedded malicious instructions.
- **Access Control**: Role-based access control preventing users from seeing unauthorized chunks.
- **Risk Engine**: Aggregates risk scores to make a final allow/block decision.
- **Context Filtering**: Limits token usage and removes unnecessary context.
- **Output Filtering**: Checks the final LLM response for sensitive patterns before returning it to the user.
