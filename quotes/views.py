import unicodedata

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import FormView, TemplateView
import requests
from twilio.rest import Client, TwilioException
from twilio.twiml.messaging_response import MessagingResponse

from .forms import SendTextForm


def get_quote() -> dict:
    """Call RapidAPI and return the retrieved response in dict"""
    url = 'https://quotes15.p.rapidapi.com/quotes/random/'
    params = {'language_code': 'en'}
    headers = {
        'x-rapidapi-host': 'quotes15.p.rapidapi.com',
        'x-rapidapi-key': settings.RAPID_API_KEY,
    }
    try:
        response = requests.get(url, params=params, headers=headers)
    except requests.RequestException:
        return {}
    return response.json()


def format_quote_response(quote_response: dict) -> str:
    if not quote_response:
        return 'Sent through Twilio API!'
    content = quote_response['content']
    normalized_content = unicodedata.normalize('NFKD', content)
    originator_name = quote_response['originator']['name']
    return f'"{normalized_content}" ({originator_name})'


class TextSuccessView(TemplateView):
    template_name = 'quotes/text_success.html'


class SendTextFormView(FormView):
    template_name = 'quotes/text.html'
    form_class = SendTextForm
    success_url = reverse_lazy('text_success')

    def form_valid(self, form):
        client = Client(settings.TWILIO_ACCOUNT_SID,
                        settings.TWILIO_AUTH_TOKEN)
        quote_response = get_quote()
        text_body = format_quote_response(quote_response)
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


@require_http_methods(['POST'])
@csrf_exempt
def handle_inbound_sms(request):
    """Send a dynamic reply to an incoming text message"""
    body: str = request.POST.get('Body', '')
    response = MessagingResponse()
    if body.lower().startswith('wahoowa'):
        response.message('WAHOOWA')
    else:
        response.message('Hi there!')
    return HttpResponse(str(response))
