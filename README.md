# Evidence checklist

Add screenshots **after** real execution (and redact account IDs, emails, credentials and tokens):

1. AWS CloudFormation stack and deployed resources.
2. DynamoDB table keys and sample anonymized request record.
3. API Gateway routes and configured JWT authorizer.
4. Lambda successful log entry and CloudWatch alarm.
5. HTTP 401 without token; HTTP 201 create; HTTP 200 get/update; HTTP 404 cross-user attempt.
6. AWS cost or budget screenshot with sensitive details redacted.

Update `docs/test-plan.md` with actual results, date, and screenshot names.
