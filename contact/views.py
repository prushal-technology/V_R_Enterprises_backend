from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ContactMessage
import json
import os

@method_decorator(csrf_exempt, name='dispatch')
class ContactFormView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            phone = data.get('phone')
            message = data.get('message')

            # Save to DB
            ContactMessage.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                message=message,
            )

            # Site owner emails and sender from .env
            site_owner_emails = os.getenv('SITE_OWNER_EMAILS', '').split(',')
            sender_email = os.getenv('EMAIL_HOST_USER')

            # 1️⃣ Email to site owners
            send_mail(
                subject=f"New Contact Message from {first_name} {last_name}",
                message=(
                    f"Name: {first_name} {last_name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n\n"
                    f"Message:\n{message}"
                ),
                from_email=sender_email,
                recipient_list=site_owner_emails,
                fail_silently=False,
            )

            # 2️⃣ Acknowledgment email to the user
            send_mail(
                subject="Thanks for contacting V R Enterprises!",
                message=(
                    f"Hi {first_name},\n\n"
                    "Thank you for reaching out to us. We have received your message and will get back to you shortly.\n\n"
                    "Best regards,\n"
                    "V R Enterprises Team."
                ),
                from_email=sender_email,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'success': True, 'message': 'Message sent successfully!'})

        except Exception as e:
            print("Error:", e)
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Use POST to send data'}, status=405)
