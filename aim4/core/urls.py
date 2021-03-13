
from django.conf.urls import url, include
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [

    path('privacy_policy/', TemplateView.as_view(template_name='corp/privacy_policy.html'), name='privacy_policy'),
    path('terms_of_service/', TemplateView.as_view(template_name='corp/terms_of_service.html'), name='terms_of_service'),

]



