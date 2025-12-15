# MVP Scope: Safe Launch

**Goal**: Avoid previous failures (data loss, race conditions, bad UX) by cutting scope to the bare minimum valid product.

## 1. Feature List (Included)
- **Club Management**: Create, Set Price (Static), Link Group (Token).
- **Membership**: Join Request, Approve/Reject.
- **Billing**: Manual Open/Close period.
- **Payments**: P2P, Manual Image Upload, Hash Deduplication.
- **Admin Tools**: Kick member (updates DB + bans in TG).

## 2. Cut List (Deferred)
- **OCR/AI**: Owner visually verifies all screenshots.
- **Automatic Period Rotation**: Owner must click "Start Month".
- **Partial Payments**: All or nothing.
- **Multi-currency**: KZT only.
- **Recurring Payment Integration**: None.
- **Web UI**: Telegram only.
- **Stats/Charts**: Text summaries only.

## 3. Previous Failure Prevention
| Failure | Fix in MVP |
| :--- | :--- |
| **Heuristic Linking** | Token-based linking ONLY. |
| **Repo Commits** | Linter rules + UoW pattern. |
| **Silent Failures** | Sentry/Logfire integration + Global Error Handler. |
| **Polling Blockage** | `taskiq` for all image processing. |
