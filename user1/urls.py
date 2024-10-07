from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
    path('',views.index),
    path('signin.html',views.signin,name='signin'),
    path('loan.html',views.backward),
    path('reg.html',views.registration,name='reg'),
    path('',views.logout,name='logout'),
    path('cibil.html',views.checkcibil,name='cibil'),
    path('update',views.userdetailupdate,name='update'),
    path('edituser',views.editfunction,name='edit'),
    path('otp/<int:id1>/',views.changepassword,name='otp'),
    path('updatepass',views.updatepassword,name='updatepass')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)