# Acceptance test plan

Record observed results and screenshots in evidence/. Do not claim success before execution.

| ID | Test | Expected | Actual |
|---|---|---|---|
| T01 | GET /requests without JWT | 401 | Not run |
| T02 | Authenticated POST /requests | 201 and requestId | Not run |
| T03 | Authenticated GET /requests | 200 with owner records | Not run |
| T04 | GET /requests/{requestId} | 200 for owner | Not run |
| T05 | PATCH status to in_progress | 200 with update | Not run |
| T06 | POST invalid category | 400 | Not run |
| T07 | Second user GET another user's request | 404 | Not run |
| T08 | Inspect Lambda CloudWatch logs | Records without secrets | Not run |
| T09 | View CloudWatch error alarm | Alarm exists | Not run |
| T10 | sam delete | Stack deleted | Not run |
