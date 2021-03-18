# Create your views here.

from django.views.generic import TemplateView
from sms.models import Order


class SMSView(TemplateView):
    template_name = "response.xml"
    content_type = "text/xml"
    def post(self, request, *args, **kwargs):
        context = dict()
        oPost = request.POST.copy()
        try:
            oOrder = Order.objects.get(phone = oPost['from'])
        except:
            oOrder = Order(phone = oPost['from'], data={"state":"WELCOMING"})
        context['aReturn'] = oOrder.handleInput(oPost['body'])
        if oOrder.isDone():
            oOrder.delete()
        else:
            oOrder.save()
        return self.render_to_response(context)
