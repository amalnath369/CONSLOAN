from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns=[
        path('laf/',views.LAFapply,name='LAF'),
        path('adminlogin',views.adminlogin,name='admin'),
        path('customerdetails.html',views.customerdetails,name='custdetail'),
        path('customerapplications.html',views.customerapplication,name='custappl'),
        path('logout',views.logout,name='loggout'),
        path('admi/<int:id1>',views.approvemail,name='approve'),
        path('admi/reject/<int:id1>',views.rejectemail,name='reject'),
        path('customerdisbursed.html',views.customerdisbursed,name='disbursed'),
        path('myaccounts.html',views.myaccounts,name='accounts'),
        path('paymentindex.html/<int:id1>',views.payment,name='payment'),
        path('paymentsuccess.html',views.paymentsuccess,name='paid'),
        path('pendingemi.html',views.pendingemi,name='pending'),
        path('empreg.html',views.empreg,name='empreg'),
        path('empdetails.html',views.empdetails,name='empdetail'),
        path('empapplications',views.empapplications,name='empapplication')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)