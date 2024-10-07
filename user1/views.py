from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import *
from mockcibil.models import *
import datetime
from datetime import datetime
import random
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == 'POST':
        email1 = request.POST.get('email')
        password1 = request.POST.get('pass')
        try:
            obj = user_reg.objects.filter(email=email1, password=password1)
            if obj:
                request.session['user_id'] = obj.first().id
                return render(request, 'index1.html', {'name': obj.first().name, 'id': obj.first().id})
            else:
                return render(request, 'sign.html', {'error_2': 'Invalid Email or Password..'})
        except Exception as e:
            return render(request, 'sign.html', {'error_2': f'An error occurred: {str(e)}'})
    return render(request, 'sign.html')

def backward(request):
    return render(request, 'index.html')

def registration(request):
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
            if user_reg.objects.filter(email=email1).exists():
                return render(request, 'reg.html', {'error_1': 'Email Already Exists!!!!..'})

            if password1 == confirm_pass:
                user_reg.objects.create(
                    name=name1,
                    email=email1,
                    phone=phone1,
                    address=address1,
                    dob=dob1,
                    gender=gender1,
                    password=confirm_pass
                )
                return render(request, 'sign.html')
            else:
                return render(request, 'reg.html', {'error_2': 'Passwords do not match.'})
        except Exception as e:
            return render(request, 'reg.html', {'error_2': f'An error occurred: {str(e)}'})
    
    return render(request, 'reg.html')

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'index.html')

def checkcibil(request):
    return render(request, 'cibil.html')

def editfunction(request):
    idv = request.session.get('user_id')
    try:
        obj = user_reg.objects.get(id=idv)
        return render(request, 'edituser.html', {'obj': obj})
    except user_reg.DoesNotExist:
        return HttpResponse("User not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

def userdetailupdate(request):
    if request.method == 'POST':
        id1 = request.POST.get('id')
        name1 = request.POST.get('name')
        address1 = request.POST.get('address')
        dob1 = request.POST.get('dob')
        email1 = request.POST.get('email')
        gender1 = request.POST.get('gender')

        try:
            obj = user_reg.objects.get(id=id1)
            if dob1:
                date_obj = datetime.strptime(dob1, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%Y-%m-%d')
                obj.dob = formatted_date
            
            obj.name = name1
            obj.address = address1
            obj.email = email1
            obj.gender = gender1
            obj.save()
            return redirect('index1')  # Change as needed
        except user_reg.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        except Exception as e:
            return render(request, 'edituser.html', {'error': f'An error occurred: {str(e)}'})

def changepassword(request, id1):
    if request.method == 'GET':
        try:
            obj = user_reg.objects.get(id=id1)
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
                print("Email sent successfully.")
            except Exception as e:
                return HttpResponse(f"Failed to send email: {e}", status=500)
        except user_reg.DoesNotExist:
            return HttpResponse("User not found.", status=404)
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    elif request.method == 'POST':
        enterdotp = request.POST.get('otp')
        createdotp = request.session.get('otp')
        if enterdotp == str(createdotp):
            return render(request, 'passwordchange.html', {'id': id1})
        else:
            return HttpResponse("Invalid OTP, Please try again")
    
    return render(request, 'otp.html', {'id': id1})

def updatepassword(request):
    if request.method == 'POST':
        id1 = request.POST.get('id')
        pass1 = request.POST.get('newpassword')
        pass2 = request.POST.get('repeatpassword')

        try:
            obj = user_reg.objects.get(id=id1)
            if pass1 == pass2:
                obj.password = pass2
                obj.save()
                return redirect('signin')
            else:
                return render(request, 'passwordchange.html', {'id': id1, 'error': 'Passwords do not match.'})
        except user_reg.DoesNotExist:
            return render(request, 'passwordchange.html', {'id': id1, 'error': 'User not found.'})
        except Exception as e:
            return render(request, 'passwordchange.html', {'id': id1, 'error': f'An error occurred: {str(e)}'})
    
    return render(request, 'passwordchange.html', {'id': id1, 'error': 'Invalid request method.'})
