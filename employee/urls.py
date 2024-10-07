from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('emplogin',views.employeelogin,name='employee'),
    path('empuserreg',views.empuserregistration,name='regg'),
    path('empuserlaf',views.empLAFapply,name='emplaf'),
    path('emppass/<int:id1>/',views.empchangepassword,name='emppass'),
    path('empupdate',views.empupdatepassword,name='empupdate')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)