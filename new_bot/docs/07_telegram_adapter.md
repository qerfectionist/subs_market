# Telegram UI Adapter

**Role**: Pure UI. No business logic.
**Stack**: `aiogram 3.x`, `redis` (FSM).

## 1. Architecture
- **Middlewares**:
    - `AuthMiddleware`: Resolves User from DB.
    - `UseCaseMiddleware`: Injects Use Case Executors.
- **Routers** (grouped by feature):
    - `onboarding_router`: `/start`, Registration.
    - `club_router`: `/create_club`, `/link_group`.
    - `member_router`: `/pay` (Upload photo), `/status`.
    - `admin_router`: callbacks for `approve_payment`, `kick`.

## 2. Handler Responsibility
1.  **Parse**: Extract data from Message/Callback.
2.  **Validate**: Check formats (is this a photo? is text len < 100?).
3.  **Execute**: Call `UseCase.execute(DTO)`.
4.  **Render**: Map `UseCaseResult` to Text/Keyboard.

## 3. UI Flows
### Member: Payment
1.  Bot sends: "Period Open. Please pay 1500 KZT." (Button: "I Paid")
2.  User clicks "I Paid".
3.  Bot asks: "Send screenshot."
4.  User sends Photo.
5.  Handler -> `SubmitPaymentProof(photo_id)`.
6.  Bot replies: "Received. Waiting for Owner approval."

### Owner: Verification
1.  Bot sends: "New Proof from @User. Hash: abc1234." (Photo + Buttons: "Approve", "Reject").
2.  Owner clicks "Approve".
3.  Handler -> `ConfirmPayment(proof_id)`.
4.  Bot updates message: "Confirmed ✅".
