from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from twilio.rest import Client, TwilioException

from .forms import SendTextForm


class TextSuccessView(TemplateView):
    template_name = 'quotes/text_success.html'


class SendTextFormView(FormView):
    template_name = 'quotes/text.html'
    form_class = SendTextForm
    success_url = reverse_lazy('text_success')

    def form_valid(self, form):
        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)
        text_body = 'Sent through Twilio API!'
        recipient_number = form.cleaned_data['number']
        try:
            client.messages.create(
                body=text_body,
                from_=settings.TWILIO_FROM_NUMBER,
                to=f'+1{recipient_number}',   # Support only US for now
            )
        except TwilioException:
            form.add_error(None, 'Failed to send the text :(')
            return self.form_invalid(form)
        return super().form_valid(form)


class HomeView(TemplateView):
    template_name = 'quotes/home.html'
