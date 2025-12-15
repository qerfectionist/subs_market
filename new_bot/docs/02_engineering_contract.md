# Engineering Contract: Architecture & Rules

## 1. Rules & Acceptance Criteria

| Rule | Rationale | Acceptance Criteria (AC) | Example Violation | Detection |
| :--- | :--- | :--- | :--- | :--- |
| **Telegram is UI Only** | Decoupling. If TG bans the bot, business data survives. | Text/Callbacks mapped to Commands. No business logic in handlers. | `if message.text == 'pay': update_db()` in handler. | Linter: prohibit DB calls in `handlers/` |
| **No DB in UI Layer** | Separation of Concerns. | UI calls Application Service/Use Case only. | Importing `SQLAlchemy` models in `handlers/`. | Import guard (e.g., `layers-lint`). |
| **Repositories: No Commits** | Transaction boundaries must be controlled by Use Cases. | `repo.add()` works, but `session.commit()` is NOT in repo. | `repo.save(user); session.commit()` | Grep `commit` in `repositories/`. |
| **One Use Case = One Tx** | Atomicity and Consistency. | Logic wrapped in `uow.commit()` block. Failure rolls back all. | Partial state update if error occurs middle-flow. | Decorator/Middleware check. |
| **Link via One-Time Token** | Security & Mapping. | Group ID is associated with Club ID only after valid token exchange. | Hardcoding Group ID or trusting user input without token. | Integration Test. |
| **Exactly Two Admins** | Control & Anti-takeover. | Bot enforces: Admin list = [Bot, Owner]. Demotes others. | Random user becomes admin. | Periodic background check. |
| **No Heavy Ops in Polling** | Availability. | OCR, Broadcasting, Reports -> Background Workers (Celery/Kiq). | `await perform_ocr()` inside `async def handler`. | Timeouts in polling logs. |
| **No Silent Failures** | Debuggability. | errors logged with trace + user notified "System Error". | `try: ... except: pass` | Linter `flake8-bugbear`. |

## 2. Automated Checks Strategy
To enforce these rules, we will implement:

1.  **Architecture Linter**:
    - `import-linter`: Forbid `infrastructure.database` imports in `ui.telegram`.
    - `flake8`: Forbid `session.commit()` in files matching `*repository.py`.
2.  **Middleware**:
    - `Use Case Decorator`: Automatically manages Transaction/UnitOfWork context.
3.  **Background Monitors**:
    - `HealthCheck`: Verifies Bot permissions and Admin count in linked groups daily.
