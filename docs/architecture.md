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
- **IAM**: Lambda uses a table-scoped policy 
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
## ADR-002 — Least-Privilege IAM Security Hardening

**Status:** Implemented and functionally verified — November 24, 2026

### Business Problem
The original AWS SAM `DynamoDBCrudPolicy` granted more DynamoDB operations than the CloudOps Service Desk Lambda application required.

### Security Implementation
Replaced the broad policy with a custom IAM statement granting four DynamoDB operations against the project's RequestsTable:

- `dynamodb:PutItem` — Create service requests.
- `dynamodb:GetItem` — Retrieve an individual request.
- `dynamodb:Query` — List requests owned by the authenticated employee.
- `dynamodb:UpdateItem` — Update request status.

The deployed Lambda role's inline policy was inspected. No directly attached managed IAM policies were found.

### Regression Testing
Following deployment, the application passed authenticated POST, individual GET, list GET, and PATCH tests.

A separate IAM Security Regression Test ticket was created and updated to `in_progress`. The original VPN Connection Failure ticket remained `resolved`.

CloudWatch Lambda logs were inspected, with no IAM permission errors observed during the reported review.

### Security Outcome
The application retains the DynamoDB operations required by its current functionality while reducing unnecessary database permissions.

### Limitations
Cross-user authorization testing is pending. The test results do not establish a complete production security assessment or validate every possible IAM permission path.