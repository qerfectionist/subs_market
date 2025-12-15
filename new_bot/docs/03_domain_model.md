# Domain Model & ERD

## 1. Entities

- **Tenant**: Isolation level (potentially for future SaaS scaling, currently typically 1 key tenant).
- **User**: Telegram User.
- **SubscriptionService**: Catalog item (e.g., "Netflix Premium", "Spotify Family").
- **SubscriptionTariff**: Specific configuration (e.g., "4 Screens, 4K").
- **Club**: The core entity. An instance of a shared subscription.
- **ClubGroup**: Mapping between Club and Telegram Chat.
- **BillingPeriod**: A specific time range (e.g., "Oct 1 - Oct 30") where money is collected.
- **ClubMember**: Link between User and Club.
- **MemberPeriod**: The state of a *specific* member in a *specific* billing period (Paid/Unpaid).
- **PaymentProof**: Screenshot evidence.
- **Dispute**: Issue raised by member.

## 2. ERD Description & Cardinality

`Tenant` (1) -- (*) `Club`
`Club` (1) -- (1) `ClubGroup`
`Club` (1) -- (*) `ClubMember`
`Club` (1) -- (*) `BillingPeriod`
`BillingPeriod` (1) -- (*) `MemberPeriod`
`ClubMember` (1) -- (*) `MemberPeriod`
`MemberPeriod` (1) -- (0..1) `PaymentProof`

## 3. Schema Specifications

### `clubs`
- `id`: UUID (PK)
- `owner_id`: FK(users)
- `service_id`: FK
- `monthly_price`: Integer (KZT)
- `max_members`: Integer
- `status`: Enum (Recruiting, Active, Paused, Closed)

### `billing_periods`
- `id`: UUID (PK)
- `club_id`: FK(clubs)
- `start_date`: Date
- `end_date`: Date
- `total_amount_target`: Integer
- `status`: Enum (Planned, Open, Closing, Closed)
- **Constraint**: Unique(`club_id`, `year`, `month`)

### `member_periods`
- `id`: UUID (PK)
- `period_id`: FK(billing_periods)
- `member_id`: FK(club_members)
- `amount_due`: Integer
- `status`: Enum (Pending, Submitted, Confirmed, Overdue, Removed)
- **Constraint**: Unique(`period_id`, `member_id`)

### `payment_proofs`
- `id`: UUID (PK)
- `member_period_id`: FK(member_periods)
- `file_id`: String (Telegram File ID)
- `image_hash`: String (Perceptual Hash)
- **Constraint**: Unique(`image_hash`, `period_id`) - Deduplication within cycle.

## 4. Indexes
- `users(telegram_id)`
- `club_groups(telegram_chat_id)`
- `payment_proofs(image_hash)`
- `billing_periods(club_id, status)`
