from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OtpToken
from django.core.mail import send_mail
from .email import emailTemplate

# Post-save signal
@receiver(post_save, sender=OtpToken)
def post_save_post(sender, instance, created, **kwargs):
    subject = "Studybuddy : Otp to Verify  your account"

    message =emailTemplate(instance.otp)
    recipient_list = [instance.email]
    send_mail(
        subject,
        "",
        html_message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list 
    )
    