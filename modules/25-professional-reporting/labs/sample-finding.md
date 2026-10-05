# RT-001 - Broken object-level authorization exposes another user's record

**Severity:** High (training example only)

**Affected asset(s):** `http://127.0.0.1:8130/api/v1/orders/{id}`

## Summary
An authenticated low-privilege user can request an order belonging to another user by changing the object identifier. The server authenticates the caller but does not enforce authorization against the requested order.

## Technical details
The endpoint trusts the requested order ID after authentication and does not verify that the order owner matches the authenticated identity.

## Evidence
- [evidence:raw/RT-001-baseline.txt]
- [evidence:raw/RT-001-cross-user.txt]

## Reproduction
1. Authenticate as the training user `alice`.
2. Request Alice's own order and record the baseline response.
3. Change only the order identifier to Bob's training order.
4. Observe that the API returns Bob's record to Alice.

## Impact
A low-privilege authenticated user may access records owned by other accounts, creating confidentiality and privacy exposure. Business impact depends on the sensitivity and breadth of accessible objects.

## Remediation
Enforce object-level authorization server-side on every request. Resolve the object, verify the authenticated principal is authorized for that object/action, and deny access by default. Add automated negative authorization tests.

## Validation / Retest
- Status: Not retested
- Evidence: Pending
