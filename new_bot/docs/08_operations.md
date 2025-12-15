# Operations & SRE

## 1. Background Job Queue (TaskIQ/Celery)
We offload all non-essential and heavy tasks.

- **Queue: `default`**:
    - `BroadcastNotification`: Sending messages to 100 users.
    - `SyncGroupPermissions`: Checking admin rights.
- **Queue: `processing`**:
    - `ProcessScreenshot`: Calculating perceptual hash (CPU intensive).
    - `OCRAnalysis`: Extracting amount/date from screenshot (optional, future).

## 2. Monitoring Signals
| Signal | Type | Alert Threshold | Rationale |
| :--- | :--- | :--- | :--- |
| `update_processing_time` | Histogram | p95 > 2s | Polling loop blocked? |
| `job_failure_rate` | Gauge | > 1% | Background workers failing. |
| `db_pool_saturation` | Gauge | > 80% | Connection leaks. |
| `transaction_errors` | Counter | spike | Logic bugs. |

## 3. Failure Scenarios
- **Telegram Down**:
    - *Impact*: UI unavailable.
    - *Recovery*: System waits. State in DB preserved.
    - *Action*: Retry broadcast jobs with exponential backoff.
- **Bot Kicked from Group**:
    - *Detection*: `BotKicked` update or API error.
    - *Action*: Mark `ClubGroup` as `UNLINKED`. Pause Billing. Notify Owner via Private Chat.
