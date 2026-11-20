# Acceptance test plan

Record actual outcomes and screenshots in `evidence/`. Do not claim any test passed until executed.

| ID | Test | Expected result | Actual | Evidence |
|---|---|---|---|---|
| T01 | Call GET /requests without JWT | 401 | Not run | — |
| T02 | Authenticated POST /requests with valid body | 201 with requestId and open status | Not run | — |
| T03 | Authenticated GET /requests | 200 with owner's requests only | Not run | — |
| T04 | GET /requests/{requestId} | 200 for owner | Not run | — |
| T05 | PATCH status to in_progress | 200 with updated status | Not run | — |
| T06 | POST invalid category | 400 | Not run | — |
| T07 | Second user attempts GET another user's request | 404 | Not run | — |
| T08 | Inspect CloudWatch request logs | Log events visible, no tokens | Not run | — |
| T09 | View CloudWatch alarm resource | Alarm exists, no notification configured | Not run | — |
| T10 | sam delete | Stack removed, check remaining billable resources | Not run | — |
