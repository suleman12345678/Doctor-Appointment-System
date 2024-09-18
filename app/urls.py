from django.urls import path
from .views import homeTemplateView, AppoinmentTemplateView, ManageAppoinmentTemplateView
urlpatterns = [
    path("", homeTemplateView.as_view(), name="home"),
    path("make-an-appointment/", AppoinmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments/", ManageAppoinmentTemplateView.as_view(), name="manage"),
]