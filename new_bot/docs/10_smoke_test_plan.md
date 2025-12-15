# Smoke Test Plan (MVP Quality Gate)

**Version:** 1.0  
**Scope:** MVP Core Flows Manual Verification  
**Goal:** Validate contract compliance and critical paths without deployment.

## 1. Preconditions & Setup
*   **Database:** Local PostgreSQL instance running (`make db` or docker-compose).
*   **Environment:** `.env` configured with `BOT_TOKEN` and `DATABASE_URL`.
*   **Test Actors:**
    *   **User A (Owner):** Telegram Account A.
    *   **User B (Member):** Telegram Account B.
    *   **Group G:** A Telegram group where User A is admin and Bot is admin.
*   **Data Stubbing:**
    *   `DEFAULT_TENANT_ID` is used (hardcoded in handlers).

---

## 2. Test Cases

### TC-01: User Initialization & Identity Mapping
**Actor:** User A & User B  
**Action:** Send `/start` to the bot.  

**Expected UI:**
*   Bot replies: "👋 Welcome to Subscription Clubs Bot!..."

**Expected DB State:**
*   `users` table: New row created for Telegram ID of User A (if first time).
*   `users` table: `user_id` (UUID) is generated and persisted.
*   Repeated `/start`: No new row, logs show `is_new=False`.

**Expected Logs:**
*   `INFO:src.ui.telegram.handlers.onboarding:Start: tg_id=... user_id=... is_new=True`

---

### TC-02: Create Club (Happy Path)
**Actor:** User A  
**Action:**
1.  `/create_club`
2.  Input Title: "Netflix Family"
3.  Input Price: "500"

**Expected UI:**
*   Bot replies: "✅ Club Created Successfully!" containing `Club ID` and `Link Token`.

**Expected DB State:**
*   `clubs` table: New row with `title="Netflix Family"`, `price_amount=500`.
*   `club_members` table: User A added as owner (`is_owner=True`).
*   `one_time_tokens` table (if implemented) or cache: Token is valid.

**Contract Check:**
*   `ensure_user` was called before creation.
*   Operation ran in single UoW transaction.

---

### TC-03: Link Telegram Group
**Actor:** User A (in Group G)  
**Action:**
1.  Add Bot to Group G.
2.  Promote Bot to Admin.
3.  Send `/link_group <TOKEN_FROM_TC-02>` in Group G.

**Expected UI:**
*   Bot replies: "✅ Group successfully linked to the Club!"

**Expected DB State:**
*   `club_groups` table: New row linking `club_id` and `telegram_chat_id` of Group G.
*   Constraint: Unique `telegram_chat_id`.

---

### TC-04: Join Club
**Actor:** User B  
**Action:**
1.  User B clicks Invite Link (simulated via `/join <CLUB_ID>`).
2.  Sending `/join <CLUB_ID_FROM_TC-02>`.

**Expected UI:**
*   Bot replies status (e.g., "Join Status: ACTIVE" or "PENDING").

**Expected DB State:**
*   `club_members` table: New row for User B (`is_owner=False`).

---

### TC-05: Open Billing Period
**Actor:** User A  
**Action:** `/open_billing <CLUB_ID>`

**Expected UI:**
*   Bot replies: "📅 Billing Period Opened" with `Period ID`.

**Expected DB State:**
*   `billing_periods` table: New row with `status='OPEN'` for current month.
*   `member_periods` table: Rows created for User A (Owner? depends on logic) and User B (Member) with `status='WAITING_FOR_PAYMENT'`.

---

### TC-06: Submit Payment Proof
**Actor:** User B  
**Action:**
1.  `/pay`
2.  Upload a screenshot/image.

**Expected UI:**
*   Bot replies: "🧾 Payment Proof Submitted".

**Expected DB State:**
*   `payment_proofs` table: New row with `screenshot_hash`.
*   `member_periods` table: User B's row updated to `status='WAITING_FOR_APPROVAL'`.
*   **Dedup Check:** Uploading the *exact same* image again should fail or return idempotent success without new DB row (if hash collision check exists). Application error "Conflict" expected if strict unique constraint on hash/period exists.

---

### TC-07: Confirm Payment
**Actor:** User A  
**Action:** `/confirm_payment <PROOF_ID> 1`

**Expected UI:**
*   Bot replies: "Payment confirmation processed."

**Expected DB State:**
*   `member_periods` table: User B's row updated to `status='PAID'` (or `ACTIVE`).
*   `payment_proofs` table: Status linked/updated if applicable.

---

### TC-08: Raise Dispute & Resolution
**Actor:** User B  
**Action:**
1.  `/dispute`
2.  Reason: "Owner did not renew Netflix."

**Expected UI:**
*   Bot replies: "Dispute opened successfully."

**Expected DB State:**
*   `disputes` table: New row with `status='OPEN'`, `reason`.
*   `dispute_events` table: Event logged 'CREATED'.

**Actor:** Admin/System (simulated via code or specialized handler)
**Action:** Call `resolve_dispute` use case.
**Expected DB State:**
*   `disputes` table: `status='RESOLVED'`.
*   `dispute_events` table: Event logged 'RESOLVED'.

---

## 3. Contract Verification Audit
This section defines manual code/architecture reviews to perform during smoke testing.

### A. UI/Infrastructure separation
*   **Check:** Verify `src/ui/telegram/handlers/*.py` contains **ZERO** imports from `sqlalchemy`, `src/infrastructure/database`, or `src/domain/entities` (except via DTOs if leaked, but strictly prefer DTOs).
*   **Pass Criteria:** Handlers only import `aiogram`, `src/application/use_cases`, `src/application/dtos`, `src/ui/telegram/presenters`.

### B. Transaction Boundaries
*   **Check:** Verify `src/application/use_cases/*.py` has exactly **ONE** `async with uow:` block.
*   **Check:** Verify `uow.commit()` is called exactly once at end of happy path.
*   **Check:** Verify `src/infrastructure/database/repositories/*.py` contain **NO** `commit()` calls.
*   **Pass Criteria:** Strict "One Use Case = One Transaction".

### C. FSM & State Integrity
*   **Check:** Verify state transitions (e.g., `BillingPeriod` status `OPEN` -> `CLOSED`) happen **ONLY** via Domain Methods or Domain Services called by Use Cases, never by direct field modification in UI or Repositories.

### D. Security & Permissions
*   **Check:** Verify `/confirm_payment` ensures `actor_user_id` is actually the Club Owner. (Contract: Application Layer should raise `PermissionDeniedError`, UI middleware/handler catches it).

### E. Idempotency & Deduplication
*   **Check:** `PaymentProof` table has `UniqueConstraint(billing_period_id, screenshot_hash)`.
*   **Pass Criteria:** Trying to insert duplicate proof raises DB IntegrityError -> caught by Repo -> wrapped in App ConflictError -> displayed nicely by UI.

---
**Status:** Ready for execution.
