from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        print("Send activation mail to user")
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        
        subject = "Activate your email"
        message = f"Hi {instance.username},\n\nPlease click on the link below to activate your account:\nActivation link: {activation_url}\n\nThankyou!"
        reciepient = [instance.email]
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, reciepient)
        except Exception as e:
            print(f"Failed to send email to {instance.email} : {str(e)}")
            
            
            
