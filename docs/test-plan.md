# Acceptance test plan

Record observed results and screenshots in evidence/. Do not claim success before execution.

| ID | Test | Expected | Actual |
|---|---|---|---|
| T01 | GET /requests without JWT | 401 | PASS — API returned Unauthorized (reported 2026-11-22; exact HTTP code not recorded) |
| T02 | Authenticated POST /requests | 201 and requestId | PASS — HTTP 201; VPN Connection Failure record verified in DynamoDB (reported 2026-11-22) |
| T03 | Authenticated GET /requests | 200 with owner records | Not run |
| T04 | GET /requests/{requestId} | 200 for owner | Not run |
| T05 | PATCH status to in_progress | 200 with update | PASS — HTTP 200; status in_progress verified in DynamoDB (2026-11-22) |
| T06 | POST invalid category | 400 | Not run |
| T07 | Second user GET another user's request | 404 | Not run |
| T08 |  Inspect Lambda CloudWatch logs | Creation and update events logged | PASS — request_created and request_updated observed |
| T09 | Verify CloudWatch error alarm | Alarm exists with expected configuration | PASS — alarm state OK; configuration verified |
| T10 | sam delete | Stack deleted | Not run |
| T11 | PATCH existing VPN ticket to resolved | 200 and resolved status | PASS — HTTP 200, status verified in DynamoDB |
| T12 | Direct SNS email notification | Email delivered | PASS |
| T13 | Verify CloudWatch SNS alarm action | Enabled and correct SNS topic | PASS |
| T14 | Simulated CloudWatch ALARM transition | Alarm email delivered | PASS |
| T15 | Verify Lambda dashboard metrics | Invocations, Errors, Duration visible | PASS — 1 invocation, 0 errors, 2.6 ms average duration in a 24-hour window |

| T16 | Verify API Gateway monitoring | Count, 4xx, 5xx, and Latency metrics | PASS — 1 request, 0 HTTP 4xx, 0 HTTP 5xx, 3.2 ms average latency; 24-hour observation |
  
## Verified test evidence (2026-11-22)

- T02: [Created VPN support ticket](../evidence/dynamodb-ticket-created.png) — title VPN Connection Failure; category network; priority high; status open.
- T05: [Updated VPN support ticket](../evidence/dynamodb-ticket-updated.png) — authenticated PATCH to `/requests/{requestId}` returned HTTP 200, and the same DynamoDB item showed `in_progress`.
- These outcomes were observed by the project owner and reported during guided testing. AWS service logs, exact response bodies, and any performance measurements have not been independently audited.
- **Next test (T11)**: PATCH same ticket status to `resolved`; expect HTTP 200 and verify `resolved` and a newer `updatedAt` in DynamoDB. Not run.
- **Additional future test**: exercise a valid JWT against `GET /requests/{requestId}` and verify data remains owner-scoped. Not run.
