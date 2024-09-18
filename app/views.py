from typing import Any
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from .models import Appointment
from django.views.generic import ListView
import datetime
from django.template import context
from django.template.loader import render_to_string, get_template



# Create your views here.
class homeTemplateView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["title"] = "Dr Suleman"
        return self.render_to_response(context)
    
    def post(self , request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")


        email = EmailMessage(
            subject= f"{name} from doctor family.",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER],
            reply_to=[email]
        )
        email.send()
        return HttpResponse("Email Sent Successfully")
    


class AppoinmentTemplateView(TemplateView):
     template_name = "appointment.html"

     def post(self , request):
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        message = request.POST.get("request")

        appointment = Appointment.objects.create(
             first_name=fname,
             last_name=lname,
             email=email,
             phone=mobile,
             request=message,
         )

        appointment.save()



        messages.add_message(request,messages.SUCCESS, f"Thanks {fname} for making an appointment, we will email you ASAP!")
        return HttpResponseRedirect(request.path)
     

class ManageAppoinmentTemplateView(ListView):
    template_name = "manage-appointments.html"
    model=Appointment
    context_object_name="appointments"
    login_required = True
    paginate_by=3

    def post(self , request):
        date = request.POST.get("date")
        appointment_id = request.POST.get("appointment-id")
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return HttpResponse(f"Appointment with ID {appointment_id} not found")
        appointment.accepted = True
        appointment.accepted_date = datetime.datetime.now()
        appointment.save()

        data = {
            "fname":appointment.first_name,
            "date":date,
        }

        message = get_template('email.html').render(data)
        email=EmailMessage(
            "About an appointment",
            message,
            settings.EMAIL_HOST_USER,
            [appointment.email]
        )
        email.content_subtype="html"
        email.send()

        

        messages.add_message(request, messages.SUCCESS, f"{date}")
        return HttpResponseRedirect(request.path)




    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        appointments = Appointment.objects.all()
        context.update({
            "title":"Manage Appointments"
        })
        return context

     