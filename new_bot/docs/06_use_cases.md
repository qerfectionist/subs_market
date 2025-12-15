# Use Cases & Transaction Boundaries

**Rule**: One Use Case = One Database Transaction.

## 1. CreateClub
- **Input**: `user_id`, `service_name`, `price`, `max_members`.
- **Steps**:
    1. Create `Club` entity (Status=Recruiting).
    2. Generate `one_time_token` for linking.
    3. Commit.
- **Output**: `club_id`, `link_token`.

## 2. LinkTelegramGroupByToken
- **Input**: `user_id`, `chat_id`, `token`.
- **Steps**:
    1. Find `Club` by `token`.
    2. Verify `club.owner_id == user_id`.
    3. Check `chat_id` not already linked.
    4. Create `ClubGroup`.
    5. Invalidate `token`.
    6. Commit.
- **Events**: `ClubLinked`.

## 3. SubmitPaymentProof
- **Input**: `user_id`, `chat_id`, `file_id`.
- **Steps**:
    1. Resolve `Club` from `chat_id`.
    2. Find active `BillingPeriod`.
    3. Find `MemberPeriod` for user.
    4. `PaymentProofService.deduplicate_hash()`.
    5. Update `MemberPeriod` status -> `PROOF_SUBMITTED`.
    6. Commit.
- **Events**: `ProofSubmitted` (Notify Owner).

## 4. ConfirmPayment
- **Input**: `owner_id`, `proof_id`, `verdict` (Approve/Reject).
- **Steps**:
    1. Load `PaymentProof` and `MemberPeriod`.
    2. Verify `owner_id` owns the club.
    3. If `Approve`: Status -> `CONFIRMED`.
    4. If `Reject`: Status -> `PENDING_PAYMENT`.
    5. Commit.
- **Events**: `PaymentConfirmed` / `PaymentRejected`.

## 5. OpenBillingPeriod
- **Input**: `club_id` (or triggered by System).
- **Steps**:
    1. Lock previous period.
    2. Calculate pricing/shares.
    3. Create `BillingPeriod` (Status=Open).
    4. Create `MemberPeriod` for all active members.
    5. Commit.
- **Events**: `PeriodOpened` (Broadcast to Group).
