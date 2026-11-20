# Architecture decision record (ADR-001)

## Status
Proposed; verify AWS deployment and acceptance tests before marking implemented.

## Context
A fictional three-office business receives service issues by email and phone, making requests hard to track and audit. This project creates an authenticated requests API with per-user isolation.

## Decision
Use API Gateway HTTP API with Cognito JWT authorization, Python Lambda compute, DynamoDB on-demand storage, CloudWatch logging/alarm, and AWS SAM/CloudFormation infrastructure as code.

## Rationale
- **HTTP API**: Simple JSON CRUD requirements; less functionality needed than REST API.
- **Cognito**: AWS-managed employee sign-in, with a JWT authorizer before application code runs.
- **Lambda**: No 24/7 web server to patch; scales with activity.
- **DynamoDB**: On-demand capacity for variable activity, ownerId partition key and requestId sort key to query one user's requests.
- **IAM**: Lambda uses a table-scoped policy (bundled CRUD permits more operations than handler requires; tighten later).
- **CloudWatch**: Seven-day logs and an error metric alarm without outbound notifications.
- **SAM**: Repeatable deployment, code review and deletion with CloudFormation.

## Security decisions
- Invitation-only Cognito user pool; passwords and tokens must never be committed.
- Table access uses the authenticated sub as ownerId; users cannot read or update another user's records through the API.
- HTTPS provided by API Gateway.
- DynamoDB encryption at rest.
- No credentials or tokens logged by application code.
- No administrator console, technician queue, or technician RBAC in this first version.

## Tradeoffs and future work
- Request list limited to 50 and exposes a continuation key; full cursor pagination not implemented.
- No SLA, assignment, attachments, or production restoration plan.
- Point-in-time backups disabled to control lab cost; enable for real production data.
- Add staff roles and global ticket queue with authorization and GSI before claiming a full company helpdesk.
- Consider frontend, CI/CD via OIDC, tracing, budgets, SNS notifications, and threat modeling.
