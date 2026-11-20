# Architecture decision record (ADR-001)

## Status
Proposed; verify AWS deployment and acceptance tests before marking implemented.

## Context
A fictional three-office business receives service issues by email and phone, which makes requests hard to track and audit. This project creates an authenticated requests API with per-user isolation.

## Decision
Use API Gateway HTTP API with Cognito JWT authorization, Python Lambda compute, DynamoDB on-demand storage, CloudWatch logging/alarm, and AWS SAM/CloudFormation infrastructure as code.

## Rationale
- **HTTP API**: Simple JSON CRUD requirements; less functionality needed than REST API.
- **Cognito**: AWS-managed employee sign-in, with a JWT authorizer before application code runs.
- **Lambda**: No 24/7 web server to patch; scales with activity.
- **DynamoDB**: On-demand capacity for variable activity, ownerId partition key and requestId sort key to query only one user's requests.
- **IAM**: Lambda accesses only the selected table through a table-scoped policy (the bundled CRUD policy permits more operations than this handler requires; tighten after testing).
- **CloudWatch**: Seven-day logs and an error metric alarm. Alarm has no outbound notification until SNS is configured.
- **SAM**: Repeatable deployment, code review and deletion through CloudFormation.

## Security decisions
- Cognito user pool is invitation-only in the example; user passwords and tokens must never be committed.
- Every table access uses the authenticated `sub` as ownerId; cross-account users cannot read/update one another's records through the API.
- HTTPS enforced by API Gateway endpoint.
- Data encrypted at rest through DynamoDB encryption.
- No email content or credentials logged by application code.
- There is **no administrator console, IT technician multi-user queue, or role-based technician permission** in this first version. This is a per-user request MVP, not a production helpdesk.

## Tradeoffs and future work
- DynamoDB request list is limited to 50 and exposes a continuation key; full cursor pagination is not yet implemented.
- No SLA policy, ticket assignment, attachment uploads, or production restore plan.
- PITR backups disabled to avoid extra charges in lab; enable before real production data.
- Add staff roles and global IT queue with authorization checks and a GSI before claiming a working company-wide helpdesk.
- Add customer-facing frontend, CI/CD deployment with OIDC, tracing, budgets, SNS notifications, and threat modeling in later phases.
