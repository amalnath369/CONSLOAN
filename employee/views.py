from django.shortcuts import render,redirect
from django.http import HttpResponse
from user1.models import *
from adminapp.models import employee,LAF
from mockcibil.views import mock_cibil_score
import random
from django.conf import settings
from django.core.mail import send_mail
def employeelogin(request):
    if request.method == 'POST':
        adminid = request.POST.get('email')
        password1 = request.POST.get('pass')
        try:
            obj = employee.objects.filter(empid=adminid, password=password1)
            if obj:
                empidd = obj.first().id
                request.session['emp_id'] = empidd
                return render(request, 'employeeindex.html', {'name': obj.first().name, 'empid': empidd})
            else:
                return render(request, 'employeelogin.html', {'error_2': 'Invalid Email or Password..'})
        except Exception as e:
            return render(request, 'employeelogin.html', {'error_2': f'An error occurred: {str(e)}'})
    return render(request, 'employeelogin.html')


def empuserregistration(request):
    if request.method == 'POST':
        name1 = request.POST.get('name')
        address1 = request.POST.get('address')
        dob1 = request.POST.get('dob')
        email1 = request.POST.get('email')
        phone1 = request.POST.get('phone')
        gender1 = request.POST.get('gender')
        password1 = request.POST.get('pass')
        confirm_pass = request.POST.get('pass1')
        
        try:
            obj = user_reg.objects.filter(email=email1)
            if obj:
                return render(request, 'reg.html', {'error_1': 'Email Already Exists!!!!..'})
            
            if password1 == confirm_pass:
                obj1 = user_reg.objects.create(
                    name=name1,
                    email=email1,
                    phone=phone1,
                    address=address1,
                    dob=dob1,
                    gender=gender1,
                    password=confirm_pass
                )
                obj1.save()
                emp_id = request.session.get('emp_id')
                if emp_id:
                    return redirect('emplaf')
                else:
                    return render(request, 'employeeindex.html')
            else:
                return render(request, 'reg.html', {'error_2': 'Passwords do not match.'})
        except Exception as e:
            return render(request, 'reg.html', {'error_2': f'An error occurred: {str(e)}'})
    
    return render(request, 'reg.html')


def empLAFapply(request):
    emp_id = request.session.get('emp_id')
    
    try:
        obj = employee.objects.get(id=emp_id)
        
        if request.method == 'POST':
            name1 = request.POST.get('name')
            email1 = request.POST.get('email')
            phone1 = request.POST.get('phone')
            dob1 = request.POST.get('dob')
            address1 = request.POST.get('address')
            gender1 = request.POST.get('gender')
            emp1 = request.POST.get('emp')
            pan1 = request.POST.get('pan')
            panimage1 = request.FILES.get('panimage')
            income1 = request.FILES.get('income')
            loan1 = request.POST.get('amount')
            empid1 = int(obj.empid)
            
            user1 = user_reg.objects.get(email=email1)
            if user1:
                laf = LAF.objects.create(
                    profile=user1,
                    employement_type=emp1,
                    pannumber=pan1,
                    panimage=panimage1,
                    incomeproof=income1,
                    loanamount=loan1,
                    empid=empid1
                )
                laf.save()
                return render(request, 'loanalert.html')
            else:
                return render(request, 'emploanapply.html', {'error_3': 'User does not exist.'})
    except employee.DoesNotExist:
        return render(request, 'emploanapply.html', {'error_3': 'Employee not found.'})
    except Exception as e:
        return render(request, 'emploanapply.html', {'error_3': f'An error occurred: {str(e)}'})
    
    return render(request, 'emploanapply.html')


def empchangepassword(request, id1):
    try:
        if request.method == 'GET':
            obj = employee.objects.get(id=id1)
            if obj:
                a = random.randint(1000, 9999)
                request.session['otp'] = a
                subject = 'OTP for Password Change'
                message = f"""Dear {obj.name},
                              You requested a password change for your account. Please use the following One-Time Password (OTP) to proceed:
                              OTP: {a}
                              This OTP is valid for the next 10 minutes. If you did not request this change, please ignore this email.
                              Thank you,
                              Team CONSLOAN
                           """
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [obj.email], fail_silently=False)
                except Exception as e:
                    return HttpResponse(f"Failed to send email: {e}", status=500)
        
        elif request.method == 'POST':
            enterdotp = request.POST.get('otp')
            createdotp = request.session.get('otp')
            if enterdotp == str(createdotp):
                return render(request, 'emppasswordchange.html', {'id': id1})
            else:
                return HttpResponse("Invalid OTP, Please try again")
    except employee.DoesNotExist:
        return HttpResponse("Employee not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return render(request, 'empotp.html', {'id': id1})


def empupdatepassword(request):
    if request.method == 'POST':
        id1 = request.POST.get('id')
        pass1 = request.POST.get('newpassword')
        pass2 = request.POST.get('repeatpassword')
        
        try:
            obj = employee.objects.get(id=id1)
            if pass1 == pass2:
                obj.password = pass2
                obj.save()
                return redirect('employee')
            else:
                return render(request, 'emppasswordchange.html', {'id': id1, 'error': 'Passwords do not match.'})
        except employee.DoesNotExist:
            return render(request, 'emppasswordchange.html', {'id': id1, 'error': 'Employee not found.'})
        except Exception as e:
            return render(request, 'emppasswordchange.html', {'id': id1, 'error': f'An error occurred: {str(e)}'})
    
    return render(request, 'emppasswordchange.html', {'id': id1, 'error': 'Invalid request method.'})
