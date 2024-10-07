from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('mock_cibil_score/', mock_cibil_score, name='mock_cibil_score'),
    path('',loanform,name='laf'),
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
