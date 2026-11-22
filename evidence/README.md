# Evidence checklist

Add screenshots only after real execution. Redact account IDs, emails, passwords and tokens.

1. CloudFormation stack and deployed resources.
2. DynamoDB key schema and an anonymized sample record.
3. API Gateway routes and configured JWT authorizer.
4. Lambda CloudWatch logs and metric alarm.
5. HTTP results: 401 without JWT, 201 create, 200 fetch/update, 404 cross-user request.
6. Budget screenshot with identifying information redacted.

Update docs/test-plan.md with execution dates, actual results, and screenshot filenames.

## Verified ticket workflow screenshots (2026-11-22)

- [dynamodb-ticket-created.png](dynamodb-ticket-created.png): VPN Connection Failure ticket created with HTTP 201 and status `open`.
- [dynamodb-ticket-updated.png](dynamodb-ticket-updated.png): same request updated with authenticated HTTP PATCH 200; DynamoDB displays `in_progress`.

These screenshots are lab evidence. Remaining tests are listed in [the acceptance test plan](../docs/test-plan.md). Redact any account and personal identifiers before publishing screenshots.
