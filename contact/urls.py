from django.urls import path
from .views import ContactFormView

urlpatterns = [
    path('send_email/', ContactFormView.as_view(), name='contact_form'),
]
