from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    path('share/', views.share, name='share'),
    path('about/', views.about, name='about'),

]
