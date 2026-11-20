# Evidence checklist

Add screenshots only after real execution. Redact account IDs, emails, passwords and tokens.

1. CloudFormation stack and deployed resources.
2. DynamoDB key schema and an anonymized sample record.
3. API Gateway routes and configured JWT authorizer.
4. Lambda CloudWatch logs and metric alarm.
5. HTTP results: 401 without JWT, 201 create, 200 fetch/update, 404 cross-user request.
6. Budget screenshot with identifying information redacted.

Update docs/test-plan.md with execution dates, actual results, and screenshot filenames.
