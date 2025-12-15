# Core Domain Services: Market Engine

These services enforce business logic across entities.

## 1. PriceGuardService
- **Purpose**: Prevent price gouging and ensure stability.
- **Methods**:
    - `validate_price_update(club, new_price)`: Checks if price change allowed (only for next period).
    - `check_fair_market_value(service_type, price)`: Warns if price > 150% of official tariff.

## 2. BillingPeriodEngine
- **Purpose**: Managing the lifecycle of cycles.
- **Methods**:
    - `advance_cycle(club)`: Closes old, opens new.
    - `calculate_member_share(club)`: `ceil(total_price / active_members)`.

## 3. MembershipStateMachine
- **Purpose**: Encapsulates transitions for members.
- **Methods**:
    - `process_proof(member_period, file)`: Hashes image, checks dupe, transitions to SUBMITTED.
    - `evict_defaulters(period)`: Finds OVERDUE members -> REMOVED.

## 4. PaymentProofService
- **Purpose**: Handling evidence.
- **Methods**:
    - `deduplicate_hash(hash, period_id)`: Throws if exists.
    - `store_proof_metadata(file_id, hash)`.

## 5. GroupHealthService
- **Purpose**: Monitoring the Telegram side.
- **Methods**:
    - `audit_permissions(group_id)`: Checks if Bot is Admin.
    - `sync_admin_list(group_id)`: Ensures only [Bot, Owner] are admins.
