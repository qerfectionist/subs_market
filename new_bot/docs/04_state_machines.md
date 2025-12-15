# State Machines & Transitions

Transitions must be atomic and triggered by Domain Commands.

## 1. Club Lifecycle (`Club.status`)

| From | To | Trigger | Invariants / Checks |
| :--- | :--- | :--- | :--- |
| `RECRUITING` | `ACTIVE` | `ActivateClub` | Min members reached. Admin present. |
| `ACTIVE` | `PAUSED` | `PauseClub` | No active Billing Period. |
| `PAUSED` | `ACTIVE` | `ResumeClub` | - |
| `*` | `CLOSED` | `CloseClub` | Resolve all debts/disputes. |

## 2. Billing Period Lifecycle (`BillingPeriod.status`)

| From | To | Trigger | Invariants / Checks |
| :--- | :--- | :--- | :--- |
| `PLANNED` | `OPEN` | `OpenPeriod` | Date reached OR Manual start. |
| `OPEN` | `CLOSING` | `LockPeriod` | Payment deadline passed. |
| `CLOSING` | `CLOSED` | `FinalizePeriod` | Service paid by Owner. All proofs confirmed. |

## 3. Member Period Lifecycle (`MemberPeriod.status`)

This tracks the individual member's obligation for a month.

| From | To | Trigger | Invariants / Checks |
| :--- | :--- | :--- | :--- |
| `PENDING_PAYMENT` | `PROOF_SUBMITTED` | `SubmitProof` | Image hash unique. |
| `PROOF_SUBMITTED` | `CONFIRMED` | `ConfirmPayment` | Owner Action. |
| `PROOF_SUBMITTED` | `PENDING_PAYMENT` | `RejectProof` | Owner Action. |
| `PENDING_PAYMENT` | `OVERDUE` | `MarkOverdue` | Time > Deadline. |
| `OVERDUE` | `REMOVED` | `EvictMember` | Owner/System Action. |
| `REMOVED` | `PENDING_PAYMENT` | `RestoreMember` | - |

## 4. Invariants
- **Closed Period Immutability**: Once `BillingPeriod` is `CLOSED`, no `MemberPeriod` inside it can change.
- **Single Active Period**: A Club can have only one `OPEN` period at a time (usually).
