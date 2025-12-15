from src.application.dtos import (
    CreateClubResponse, LinkGroupResponse, JoinClubResponse, 
    OpenBillingPeriodResponse, SubmitPaymentProofResponse
)

class ClubPresenter:
    @staticmethod
    def present_created(response: CreateClubResponse) -> str:
        return (
            f"✅ <b>Club Created Successfully!</b>\n\n"
            f"Club ID: <code>{response.club_id}</code>\n"
            f"Link Token: <code>{response.link_token.value}</code>\n\n"
            f"Use this token to link your Telegram Group."
        )

    @staticmethod
    def present_linked(response: LinkGroupResponse) -> str:
        if response.success:
            return "✅ Group successfully linked to the Club!"
        return "❌ Failed to link group."

    @staticmethod
    def present_club_list(clubs: list, lang: str = "ru") -> str:
        from ..i18n import get_text
        if not clubs:
            return get_text("no_clubs", lang)
        return get_text("my_clubs", lang)

class BillingPresenter:
    @staticmethod
    def present_period_opened(response: OpenBillingPeriodResponse) -> str:
        return (
            f"📅 <b>Billing Period Opened</b>\n\n"
            f"Period ID: <code>{response.billing_period_id}</code>\n"
            f"Status: {response.status.name}"
        )

    @staticmethod
    def present_proof_submitted(response: SubmitPaymentProofResponse) -> str:
        return (
            f"🧾 <b>Payment Proof Submitted</b>\n\n"
            f"ID: <code>{response.payment_proof_id}</code>\n"
            f"Status: {response.member_period_status.name}"
        )
