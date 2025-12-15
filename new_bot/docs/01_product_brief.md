# Product Brief: Subscription Clubs Platform

## 1. Goal
Create a **Telegram-based platform for shared digital subscription clubs in Kazakhstan**.
- **Nature**: Savings service, not a profit service.
- **Philosophy**: Cost sharing. Club owner is an equal participant and pays the same terms as others.
- **Financial Model**: P2P transfers only (Kaspi/Bank). No escrow, no auto-charging.
- **Proof**: Mandatory screenshot proof for every payment.
- **Resilience**: Telegram is UI only. The core system must be the source of truth and function even if Telegram disappears or accounts are banned.

## 2. Core User Roles
| Role | Responsibilities |
| :--- | :--- |
| **Club Owner (Admin)** | Creates club, sets price, accepts members, verifies payments, pays the service provider, maintains the service account. |
| **Member** | Joins club, pays their share via P2P, uploads screenshot proof, consumes service. |
| **System Bot** | Facilitates flow, enforces rules, tracks state, notifies users, audits activity. |

## 3. Core Flows
1.  **Club Creation**: Owner creates a club, sets tariff (Service Name, Price, max members), and gets a one-time link token.
2.  **Group Linking**: Owner adds Bot to a new Telegram Group and links it using the token.
3.  **Member Onboarding**: User joins the group -> Bot detects new member -> User registers in Bot -> User requests to join the Club -> Owner approves.
4.  **Billing Cycle**:
    - **Open**: Period starts. Bot calculates share (Total Price / Count).
    - **Payment**: Members send money to Owner P2P. Members upload screenshot to Bot.
    - **Verification**: Owner reviews screenshots. Owner approves or rejects.
    - **Completion**: When all collected, Owner pays service.
5.  **Dispute**: If Owner disappears or Service stops working, Members can raise a dispute.

## 4. Non-Goals (Out of Scope)
- **Marketplace**: We do not provide a search for clubs. Discovery is external.
- **Profit**: Owners cannot set a price higher than the service cost (or system enforces transparency).
- **Payment Processing**: No integration with Stripe/Kaspi Pay. Manual P2P only.
- **Service Management**: We do not manage Netflix/Spotify passwords. That is done in the chat or pinned message (manual).

## 5. Constraints & Invariants
- **Pricing**: Immutable within a billing period. New price = New Billing Period.
- **Topology**: One Club = One Telegram Group.
- **Proof**: Deduplicated by image hash.
