from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from honeypot.decorators import verify_honeypot_value
from act.hello.forms import ContactForm

MESSAGE_SENT_URL = getattr(settings, 'HELLO_MESSAGE_SENT_URL', None)

class Hello(object):
    
    def __init__(self, form=None):
        self.form_class = form if form is not None else ContactForm
    
    def __call__(self, request):
        if request.method == 'GET':
            return self.get(request)
        elif request.method == 'POST':
            return self.post(request)
        # no such method status code?
    
    def get(self, request):
        form = self.form_class()
        return render_to_response('hello/form.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

    def post(self, request):
        
        # check honeypot value manually
        honeypot = verify_honeypot_value(request, settings.HONEYPOT_FIELD_NAME)
        if honeypot:
            return honeypot
        
        # check for form validity
        form = self.form_class(request.POST)
        if form.is_valid():
            # send message on valid form submission
            self.send_message(request, form.cleaned_data)
            # notify user of success and redirect
            messages.success(request, 'Your message was successfully sent')
            return HttpResponseRedirect(MESSAGE_SENT_URL if MESSAGE_SENT_URL else request.path)
            
        # form was not valid, show errors to user
        return render_to_response('hello/form.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))
    
    def send_message(self, request, data):
        domain = Site.objects.get_current().domain
        subject = "[%s] Hello from %s" % (domain, data['name'])
        #message = render_to_string('hello/email.txt', {'contact': data})
        message = "%s\n\n%s" % (data['email'], data['comment'])
        if data['url']:
            message += '\n\n%s' % data['url']
        sender = "%s <%s>" % (data['name'], data['email'])
        recipients = [u[1] for u in settings.MANAGERS]
        send_mail(subject, message, sender, recipients)