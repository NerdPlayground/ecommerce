from django.urls import reverse
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class EcommerceAPIAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        """
        Use dj_rest_auth email verification endpoint

        Updates the send_mail context variable to include it
        """

        confirm_email_url=reverse("account_confirm_email",kwargs={"key":context.get("key")})
        base_url=context.get("activate_url").split(confirm_email_url)[0]
        verification_url=f'{base_url}{reverse("rest_verify_email")}'
        ctx={
            "verification_url":verification_url,
            "expires_after":settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS,
        }
        ctx.update(context)
        return super().send_mail(template_prefix, email, ctx)